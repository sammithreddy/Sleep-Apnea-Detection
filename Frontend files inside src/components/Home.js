import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import SleepApneaStats from "./SleepApneaStats";
import SleepApneaInfo from "./SleepApneaInfo";

function Home() {
  return (
    <Container className="mt-5 pt-4 text-center animate-fade-in">
      <Row>
        <Col>
            <h1 style={{ 
              fontWeight: "800", 
              fontSize: "3rem", 
              background: "var(--primary)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              marginBottom: "1rem"
            }}>
            🩺 Sleep Apnea Detection System
          </h1>
          <p style={{ fontSize: "1.25rem", color: "var(--secondary)", maxWidth: "700px", margin: "0 auto 3rem", lineHeight: "1.6" }}>
            AI-powered ECG analysis to detect sleep apnea & provide insightful explanations instantly.
          </p>
        </Col>
      </Row>

      {/* Sleep Apnea Information */}
      <SleepApneaInfo />

      {/* Sleep Apnea Statistics */}
      <Row className="mt-5">
        <Col>
          <SleepApneaStats />
        </Col>
      </Row>
    </Container>
  );
}

export default Home;
