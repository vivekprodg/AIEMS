"use client";

import { Form, Input, Select, Checkbox, Button, Radio, message, Spin } from "antd";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { getPrograms, getApplyCourseBanner, submitCourseApplication, resolveMediaUrl } from "@/lib/api/home";

const { Option } = Select;
const { TextArea } = Input;

export default function ApplyNowPage() {
  const [form] = Form.useForm();
  const [submitting, setSubmitting] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();
  const [programs, setPrograms] = useState([]);
  const [banner, setBanner] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    const fetchPageData = async () => {
      setLoading(true);
      try {
        const [programsList, bannerData] = await Promise.all([
          getPrograms(),
          getApplyCourseBanner()
        ]);
        if (active) {
          setPrograms(Array.isArray(programsList) ? programsList : []);
          setBanner(bannerData || {});
        }
      } catch (err) {
        console.error("[AIEMS Admissions] Error fetching page requirements:", err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    fetchPageData();
    return () => {
      active = false;
    };
  }, []);

  const sanitizeContact = (value) => {
    if (!value) return "";
    return String(value).trim().replace(/\s+/g, "");
  };

  const handleFinish = async (values) => {
    if (submitting) return;

    const contactValue = sanitizeContact(values.contactNumber);
    const programId = values.program ? Number(values.program) : null;

    setSubmitting(true);
    messageApi.loading({ content: "Submitting application details...", key: "apply_submit" });

    const payload = {
      name: values.fullName.trim(),
      gender: values.gender,
      contact: contactValue,
      email: values.email.trim().toLowerCase(),
      program: programId,
      institution: values.institution.trim(),
      message: values.message?.trim() || "",
    };

    try {
      await submitCourseApplication(payload);
      messageApi.success({
        content: "Application submitted successfully! Our counseling desk will contact you soon.",
        key: "apply_submit",
        duration: 5,
      });
      form.resetFields();
    } catch (err) {
      messageApi.error({
        content: err.message || "Unable to submit your application. Please check your connection and try again.",
        key: "apply_submit",
        duration: 5,
      });
    } finally {
      setSubmitting(false);
    }
  };

  const bannerImage = banner?.image ? resolveMediaUrl(banner.image) : null;

  return (
    <div className="scroll-smooth min-h-screen bg-gray-50/50">
      {contextHolder}

      {/* Dynamic Banner */}
      <div
        className="relative h-[380px] md:h-[450px] bg-cover bg-center bg-no-repeat flex items-center justify-center px-6 bg-secondary"
        style={bannerImage ? { backgroundImage: `url('${bannerImage}')` } : {}}
      >
        <div className="absolute inset-0 bg-black/50 z-0" />

        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="relative z-10 text-center text-white max-w-3xl"
        >
          {banner?.heading && (
            <h1 className="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight">
              {banner.heading}
            </h1>
          )}
          {banner?.sub_heading && (
            <p className="text-white/90 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
              {banner.sub_heading}
            </p>
          )}
        </motion.div>
      </div>

      {/* Dynamic Form Card */}
      <div className="relative z-20 -mt-24 md:-mt-32 px-4 md:px-8 pb-20">
        <motion.div
          className="max-w-3xl mx-auto bg-white/95 backdrop-blur-md p-8 md:p-12 rounded-2xl shadow-2xl border border-gray-150"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold text-primary mb-2">Admission Application</h2>
            <div className="h-1 w-16 bg-primary mx-auto rounded-full mb-4" />
          </div>

          <Spin spinning={loading} tip="Fetching program listings...">
            <Form
              form={form}
              layout="vertical"
              onFinish={handleFinish}
              scrollToFirstError
              requiredMark={false}
              className="space-y-6"
            >
              <Form.Item
                label="Full Name"
                name="fullName"
                rules={[{ required: true, message: "Please enter your full name" }]}
              >
                <Input size="large" placeholder="Enter your full name" className="rounded-lg h-11" />
              </Form.Item>

              <Form.Item
                label="Gender"
                name="gender"
                rules={[{ required: true, message: "Please select your gender" }]}
              >
                <Radio.Group className="flex gap-6">
                  <Radio value="male">Male</Radio>
                  <Radio value="female">Female</Radio>
                  <Radio value="other">Other</Radio>
                </Radio.Group>
              </Form.Item>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Form.Item
                  label="Contact Number"
                  name="contactNumber"
                  rules={[{ required: true, message: "Please enter your contact number" }]}
                >
                  <Input type="tel" size="large" placeholder="Contact number" className="rounded-lg h-11" />
                </Form.Item>

                <Form.Item
                  label="Email ID"
                  name="email"
                  rules={[
                    { required: true, message: "Please enter your email" },
                    { type: "email", message: "Please enter a valid email" }
                  ]}
                >
                  <Input size="large" placeholder="you@example.com" className="rounded-lg h-11" />
                </Form.Item>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Form.Item
                  label="Select Program"
                  name="program"
                  rules={[{ required: true, message: "Please select a program" }]}
                >
                  <Select size="large" placeholder="Select an academic program" className="rounded-lg h-11">
                    {programs.map((prog) => (
                      <Option key={prog.id} value={String(prog.id)}>
                        {prog.heading}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>

                <Form.Item
                  label="Previous School / College"
                  name="institution"
                  rules={[{ required: true, message: "Please enter your high school name" }]}
                >
                  <Input placeholder="High school or +2 college name" size="large" className="rounded-lg h-11" />
                </Form.Item>
              </div>

              <Form.Item label="Inquiries / Notes" name="message">
                <TextArea rows={4} placeholder="Any notes or questions..." size="large" className="rounded-lg" />
              </Form.Item>

              <Form.Item
                name="confirmation"
                valuePropName="checked"
                rules={[
                  {
                    validator: (_, value) =>
                      value === true
                        ? Promise.resolve()
                        : Promise.reject(new Error("Please confirm that all details provided are accurate.")),
                  },
                ]}
              >
                <Checkbox className="text-gray-700 text-xs sm:text-sm">
                  I confirm that all details provided are accurate.
                </Checkbox>
              </Form.Item>

              <Form.Item className="pt-2 m-0">
                <Button
                  type="primary"
                  htmlType="submit"
                  size="large"
                  loading={submitting}
                  disabled={submitting}
                  block
                  className="w-full h-12 rounded-xl text-base font-bold btn_primary_fill shadow-md transition-all"
                >
                  {submitting ? "Submitting..." : "Submit Application"}
                </Button>
              </Form.Item>
            </Form>
          </Spin>
        </motion.div>
      </div>
    </div>
  );
}