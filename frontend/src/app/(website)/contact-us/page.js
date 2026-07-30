"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FaMapPin, FaPhone } from "react-icons/fa";
import { IoMdMail } from "react-icons/io";
import { Form, Input, Button, message, Spin } from "antd";
import { submitContactInquiry, getHomeContent } from "@/lib/api/home";

const { TextArea } = Input;

export default function ContactUs() {
  const [form] = Form.useForm();
  const [submitting, setSubmitting] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();
  const [siteData, setSiteData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    const fetchSiteDetails = async () => {
      try {
        setLoading(true);
        const data = await getHomeContent();
        if (active) {
          setSiteData(data);
        }
      } catch (err) {
        console.error("Error retrieving contact page configuration:", err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    fetchSiteDetails();
    return () => {
      active = false;
    };
  }, []);

  const contactInfo = siteData?.admission_contact || {};
  const siteSettings = siteData?.site_settings || {};

  const phone = contactInfo.contact || siteSettings.primary_phone || "";
  const email = contactInfo.mail_id || siteSettings.primary_email || "";
  const address = siteSettings.location_address || "";
  const mapIframeUrl = siteSettings.map_iframe_url || "";

  const handleFinish = async (values) => {
    if (submitting) return;

    const payload = {
      name: values.name.trim(),
      email: values.email.trim().toLowerCase(),
      city: values.city.trim(),
      message: values.message?.trim() || "",
      contact: values.contact ? String(values.contact).trim().replace(/\s+/g, "") : "",
    };

    setSubmitting(true);
    messageApi.loading({ content: "Sending message...", key: "contact_submit" });

    try {
      await submitContactInquiry(payload);
      messageApi.success({
        content: "Message sent successfully! Our team will contact you soon.",
        key: "contact_submit",
        duration: 5,
      });
      form.resetFields();
    } catch (err) {
      messageApi.error({
        content: err.message || "Unable to send message. Please check your connection and try again.",
        key: "contact_submit",
        duration: 5,
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50/50">
        <Spin size="large" />
        <p className="mt-4 text-slate-600 font-medium text-sm">Loading Contact Details...</p>
      </div>
    );
  }

  return (
    <div className="w-full min-h-screen bg-gray-50/50">
      {contextHolder}

      {/* Banner Section */}
      <div className="relative w-full h-80 bg-secondary flex items-center justify-center">
        <div className="absolute inset-0 bg-black/40" />
        <div className="relative z-10 text-center text-white px-4 max-w-2xl">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-3 tracking-tight">
            Contact Us
          </h1>
        </div>
      </div>

      {/* Form & Map Section */}
      <div className="py-16 px-4 sm:px-6 lg:px-8 relative">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          
          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="bg-white rounded-2xl shadow-xl border border-gray-150 p-8 md:p-10"
          >
            <h2 className="text-2xl font-bold mb-6 text-secondary border-b border-gray-100 pb-3">
              Send an Inquiry
            </h2>
            <Form
              form={form}
              layout="vertical"
              onFinish={handleFinish}
              scrollToFirstError
              requiredMark={false}
              className="space-y-4"
            >
              <Form.Item
                label="Your Full Name"
                name="name"
                rules={[{ required: true, message: "Please enter your full name" }]}
              >
                <Input size="large" className="rounded-lg h-11" placeholder="Enter your name" />
              </Form.Item>

              <Form.Item
                label="Your Email Address"
                name="email"
                rules={[
                  { required: true, message: "Please enter your email" },
                  { type: "email", message: "Please enter a valid email address" }
                ]}
              >
                <Input size="large" className="rounded-lg h-11" placeholder="you@example.com" />
              </Form.Item>

              <Form.Item label="Contact Number" name="contact">
                <Input size="large" className="rounded-lg h-11" placeholder="Phone number" />
              </Form.Item>

              <Form.Item
                label="Your Location / City"
                name="city"
                rules={[{ required: true, message: "Please enter your city" }]}
              >
                <Input size="large" className="rounded-lg h-11" placeholder="City name" />
              </Form.Item>

              <Form.Item
                label="Inquiry Message"
                name="message"
                rules={[{ required: true, message: "Please enter your message" }]}
              >
                <TextArea rows={4} className="rounded-lg" placeholder="Write your query..." />
              </Form.Item>

              <Form.Item className="pt-2 m-0">
                <Button
                  type="primary"
                  htmlType="submit"
                  size="large"
                  loading={submitting}
                  disabled={submitting}
                  className="btn_primary_fill text-white font-bold h-12 rounded-xl transition w-full"
                >
                  {submitting ? "Sending..." : "Submit Inquiry"}
                </Button>
              </Form.Item>
            </Form>
          </motion.div>

          {/* Contact Details & Map */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="space-y-8"
          >
            <div className="bg-white rounded-2xl shadow-xl border border-gray-150 p-8 space-y-6">
              <h2 className="text-2xl font-bold text-secondary border-b border-gray-100 pb-3">
                Get in Touch
              </h2>
              
              {address && (
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-lg shrink-0 mt-0.5">
                    <FaMapPin />
                  </div>
                  <div>
                    <p className="font-bold text-secondary text-sm">Campus Address</p>
                    <p className="text-gray-600 text-xs sm:text-sm mt-0.5">{address}</p>
                  </div>
                </div>
              )}

              {phone && (
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-lg shrink-0 mt-0.5">
                    <FaPhone />
                  </div>
                  <div>
                    <p className="font-bold text-secondary text-sm">Hotline</p>
                    <a href={`tel:${phone}`} className="text-gray-600 hover:text-primary text-xs sm:text-sm mt-0.5 block font-semibold">
                      {phone}
                    </a>
                  </div>
                </div>
              )}

              {email && (
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-lg shrink-0 mt-0.5">
                    <IoMdMail className="text-xl" />
                  </div>
                  <div>
                    <p className="font-bold text-secondary text-sm">Email Address</p>
                    <a href={`mailto:${email}`} className="text-gray-600 hover:text-primary text-xs sm:text-sm mt-0.5 block font-semibold break-all">
                      {email}
                    </a>
                  </div>
                </div>
              )}
            </div>

            {/* Map Frame */}
            {mapIframeUrl && (
              <div className="overflow-hidden rounded-2xl shadow-xl h-72 border border-gray-200">
                <iframe
                  title="Campus Location Map"
                  src={mapIframeUrl}
                  width="100%"
                  height="100%"
                  style={{ border: 0 }}
                  allowFullScreen=""
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                />
              </div>
            )}
          </motion.div>

        </div>
      </div>
    </div>
  );
}