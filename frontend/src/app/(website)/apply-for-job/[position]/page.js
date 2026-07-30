"use client";

import React, { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { motion } from "framer-motion";
import { Form, Input, Radio, Select, Upload, Button, message, Spin } from "antd";
import { InboxOutlined } from "@ant-design/icons";
import { 
  getApplyPositionBanner, 
  getTeamFaculties, 
  submitVacancyApplication,
  resolveMediaUrl
} from "@/lib/api/home";

const { Option } = Select;
const { Dragger } = Upload;

export default function CareersApply() {
  const params = useParams();
  const [form] = Form.useForm();
  const [messageApi, contextHolder] = message.useMessage();
  
  const [banner, setBanner] = useState(null);
  const [vacancies, setVacancies] = useState([]);
  const [fileList, setFileList] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const currentPositionParam = params?.position;

  useEffect(() => {
    let active = true;
    
    const fetchPageData = async () => {
      try {
        setLoading(true);
        const [bannerData, facultiesData] = await Promise.all([
          getApplyPositionBanner(),
          getTeamFaculties()
        ]);

        if (active) {
          setBanner(bannerData || {});
          
          const normalizedFaculties = Array.isArray(facultiesData) 
            ? facultiesData 
            : facultiesData?.results || [];
          setVacancies(normalizedFaculties);

          if (currentPositionParam && normalizedFaculties.length > 0) {
            const matched = normalizedFaculties.find(
              (v) => String(v.id) === String(currentPositionParam)
            );
            if (matched) {
              form.setFieldsValue({ vacancy: String(matched.id) });
            }
          }
        }
      } catch (err) {
        console.error("[AIEMS Careers Form] Failed to resolve requirements:", err);
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
  }, [currentPositionParam, form]);

  const uploadProps = {
    name: "document",
    multiple: false,
    maxCount: 1,
    fileList: fileList,
    beforeUpload: (file) => {
      const allowedMimeTypes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ];
      
      const fileExtension = file.name.split(".").pop().toLowerCase();
      const isValidExtension = ["pdf", "doc", "docx"].includes(fileExtension);
      const isValidMime = allowedMimeTypes.includes(file.type);

      if (!isValidMime && !isValidExtension) {
        messageApi.error(`${file.name} is not a valid document. Formats allowed: PDF, DOC, or DOCX.`);
        return Upload.LIST_IGNORE;
      }

      const isLt5M = file.size / 1024 / 1024 < 5;
      if (!isLt5M) {
        messageApi.error("Resume document size must not exceed 5MB.");
        return Upload.LIST_IGNORE;
      }

      setFileList([file]);
      return false;
    },
    onRemove: () => {
      setFileList([]);
    }
  };

  const onFinish = async (values) => {
    if (submitting) return;

    if (fileList.length === 0) {
      messageApi.error("Please attach your CV document (PDF/DOC) to proceed.");
      return;
    }

    setSubmitting(true);
    messageApi.loading({ content: "Uploading application documents...", key: "hr_submit" });

    const formData = new FormData();
    formData.append("name", values.fullName.trim());
    formData.append("gender", values.gender);
    formData.append("contact", values.contact.trim().replace(/\s+/g, ""));
    formData.append("email", values.email.trim().toLowerCase());
    formData.append("position", values.vacancy);
    formData.append("message", values.coverMessage?.trim() || "");
    formData.append("document", fileList[0]);

    try {
      await submitVacancyApplication(formData);
      messageApi.success({
        content: "Your job application has been submitted successfully!",
        key: "hr_submit",
        duration: 5
      });
      form.resetFields();
      setFileList([]);
    } catch (err) {
      messageApi.error({
        content: err.message || "Unable to submit application. Please try again.",
        key: "hr_submit",
        duration: 5
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
        className="relative h-[380px] md:h-[450px] bg-cover bg-center bg-no-repeat flex items-center justify-center px-6 transition-all duration-500 bg-secondary"
        style={bannerImage ? { backgroundImage: `url('${bannerImage}')` } : {}}
      >
        <div className="absolute inset-0 bg-black/50 z-0" />

        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="relative z-10 text-center text-white max-w-4xl"
        >
          {banner?.heading && (
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
              {banner.heading}
            </h1>
          )}
          {banner?.sub_heading && (
            <p className="text-base md:text-xl max-w-2xl mx-auto mt-4 text-white/90 leading-relaxed">
              {banner.sub_heading}
            </p>
          )}
        </motion.div>
      </div>

      {/* Form Section */}
      <div className="relative z-20 -mt-24 md:-mt-32 px-4 md:px-0 pb-24">
        <motion.div
          className="max-w-3xl mx-auto bg-white/95 backdrop-blur-md p-8 md:p-12 rounded-2xl shadow-2xl border border-gray-150"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <div className="text-center mb-10">
            <h2 className="text-3xl font-extrabold text-primary mb-2 tracking-tight">
              Apply For a Position
            </h2>
            <div className="h-1 w-16 bg-primary mx-auto rounded-full mb-4" />
          </div>

          <Spin spinning={loading} tip="Fetching positions...">
            <Form
              layout="vertical"
              form={form}
              onFinish={onFinish}
              requiredMark={false}
              className="space-y-6"
            >
              <Form.Item
                label="Full Name"
                name="fullName"
                rules={[{ required: true, message: "Please enter your full name" }]}
              >
                <Input size="large" placeholder="Your full name" className="rounded-lg h-11" />
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
                  name="contact"
                  rules={[{ required: true, message: "Please enter your contact number" }]}
                >
                  <Input size="large" placeholder="Contact number" className="rounded-lg h-11" />
                </Form.Item>

                <Form.Item
                  label="Email ID"
                  name="email"
                  rules={[
                    { required: true, message: "Please enter your email" },
                    { type: "email", message: "Enter a valid email address" }
                  ]}
                >
                  <Input size="large" placeholder="you@example.com" className="rounded-lg h-11" />
                </Form.Item>
              </div>

              <Form.Item
                label="Target Position / Department"
                name="vacancy"
                rules={[{ required: true, message: "Please select a target position" }]}
              >
                <Select size="large" placeholder="Select a role" className="rounded-lg h-11">
                  {vacancies.map((vacancy) => (
                    <Option key={vacancy.id} value={String(vacancy.id)}>
                      {vacancy.heading}
                    </Option>
                  ))}
                </Select>
              </Form.Item>

              <Form.Item
                label="Upload Resume"
                name="resume"
                extra="Acceptable formats: PDF, DOC, or DOCX. Maximum file size: 5MB."
              >
                <Dragger {...uploadProps} className="!py-6 bg-gray-50/80 border-gray-300 rounded-xl hover:border-primary transition-colors">
                  <p className="ant-upload-drag-icon">
                    <InboxOutlined className="text-4xl text-primary" />
                  </p>
                  <p className="ant-upload-text font-semibold text-gray-700">Click or drag file here to upload</p>
                  <p className="ant-upload-hint text-gray-500 text-xs">PDF or Microsoft Word files only</p>
                </Dragger>
              </Form.Item>

              <Form.Item
                label="Cover Message"
                name="coverMessage"
                rules={[{ required: true, message: "Please write a message" }]}
              >
                <Input.TextArea
                  rows={5}
                  placeholder="Summarize your professional qualifications..."
                  className="rounded-lg"
                />
              </Form.Item>

              <Form.Item className="pt-2 m-0">
                <Button
                  type="primary"
                  htmlType="submit"
                  size="large"
                  loading={submitting}
                  disabled={loading || submitting}
                  className="btn_primary_fill w-full h-12 rounded-xl text-base font-bold shadow-md transition-all"
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