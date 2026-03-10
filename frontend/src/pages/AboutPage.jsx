import React from "react";
import { Container, Row, Col, Card, Badge } from "react-bootstrap";

function AboutPage() {
  const teamMembers = [
    { name: "Sammith Reddy", role: "Project Lead / ML Engineer" },
    { name: "Manish Reddy", role: "Full Stack Developer" },
    { name: "Maruthi Reddy", role: "Data Scientist / Documentation" },
  ];

  return (
    <Container className="mt-5 pt-4 animate-fade-in mb-5">
      <Row className="justify-content-center text-center mb-5">
        <Col md={8}>
          <Badge bg="primary" className="mb-3 px-3 py-2" style={{ borderRadius: "20px" }}>Our Story</Badge>
          <h1 style={{ fontWeight: "800", fontSize: "2.5rem", color: "var(--dark)" }}>
            About the Project
          </h1>
          <p className="lead text-muted mt-3">
            This Sleep Apnea Detection System was developed as a <strong>Major Project</strong> by students of the 
            <strong> Information Technology Department</strong> at <strong>GRIET (Gokaraju Rangaraju Institute of Engineering and Technology)</strong>.
          </p>
        </Col>
      </Row>

      <Row className="mb-5">
        <Col md={6}>
          <Card className="h-100 p-4 shadow-sm border-0">
            <h3 className="mb-4 text-primary">The Vision</h3>
            <p>
              Sleep apnea is an under-diagnosed condition affecting millions globally. Our vision was to leverage 
              modern Machine Learning techniques to provide a fast, reliable, and accessible screening tool 
              using only ECG signals.
            </p>
            <p>
              By utilizing the PhysioNet Apnea-ECG database, we've trained robust models that can identify 
              apneic events with high precision, potentially helping clinicians and patients identify risks early.
            </p>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="h-100 p-4 shadow-sm border-0">
            <h3 className="mb-4 text-primary">Academic Excellence</h3>
            <p>
              This website represents the culmination of our undergraduate studies at GRIET. We have integrated 
              complex data pipelines, signal processing algorithms, and interactive UI/UX designs to create a 
              complete end-to-end healthcare technology solution.
            </p>
            <ul>
              <li>High-accuracy XGBoost Classification</li>
              <li>Advanced HRV Feature Extraction</li>
              <li>Interactive Signal Visualization</li>
            </ul>
          </Card>
        </Col>
      </Row>

      <Row className="text-center mb-4">
        <Col>
          <h2 style={{ fontWeight: "800" }}>The Team</h2>
          <hr style={{ width: "50px", border: "2px solid var(--primary)", margin: "20px auto" }} />
        </Col>
      </Row>

      <Row className="justify-content-center">
        {teamMembers.map((member, index) => (
          <Col key={index} md={4} className="mb-4">
            <Card className="text-center p-4 border-0 shadow-sm h-100">
              <div className="mx-auto mb-3 d-flex align-items-center justify-content-center" 
                   style={{ width: "80px", height: "80px", backgroundColor: "#f0f4ff", borderRadius: "50%", color: "var(--primary)", fontSize: "2rem" }}>
                👤
              </div>
              <h5 style={{ fontWeight: "700" }}>{member.name}</h5>
              <p className="text-primary small mb-0">{member.role}</p>
              <p className="text-muted mt-2" style={{ fontSize: "0.9rem" }}>IT Department, GRIET</p>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default AboutPage;
