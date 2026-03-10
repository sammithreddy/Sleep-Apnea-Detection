import React from "react";
import { Container, Row, Col, Card } from "react-bootstrap";

function SleepApneaInfo() {
  return (
    <Container className="mt-5">
      <Row className="text-center">
        <Col>
          <h3>🌎 Global Sleep Apnea Statistics</h3>
          <p>Sleep apnea affects millions of people worldwide, leading to serious health risks if left untreated.</p>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={4}>
          <Card className="p-3 shadow-sm">
            <Card.Body>
              <h5>🛌 Affects 1 Billion People</h5>
              <p>Studies show that nearly **1 billion adults** suffer from obstructive sleep apnea (OSA).</p>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="p-3 shadow-sm">
            <Card.Body>
              <h5>⚠️ 80% Remain Undiagnosed</h5>
              <p>Most people with sleep apnea don't know they have it, increasing the risk of heart disease & stroke.</p>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="p-3 shadow-sm">
            <Card.Body>
              <h5>🚑 Linked to Major Diseases</h5>
              <p>OSA is associated with **hypertension, diabetes, and cognitive decline**.</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mt-5 text-center">
        <Col>
          <h4>🩺 Latest Advances in Sleep Apnea Treatment</h4>
          <p>New treatments are emerging, offering hope for those suffering from sleep apnea.</p>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={6}>
          <Card className="p-3 shadow-sm">
            <Card.Body>
              <h5>💊 New Drug Trials</h5>
              <p>The epilepsy drug **Sulthiame** has shown a **50% reduction** in apnea symptoms.</p>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="p-3 shadow-sm">
            <Card.Body>
              <h5>⚕️ Weight Loss Medications</h5>
              <p>Drugs like **Zepbound** are now being **approved for treating sleep apnea**.</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default SleepApneaInfo;
