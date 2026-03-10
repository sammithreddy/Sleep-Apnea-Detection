import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="mt-5 py-5" style={{ background: "#1a202c", color: "rgba(255,255,255,0.7)" }}>
      <Container>
        <Row className="gy-4">
          <Col md={4}>
            <h5 className="text-white mb-3" style={{ fontWeight: "800" }}>
              🩺 ApneaDetect
            </h5>
            <p style={{ fontSize: "0.9rem", lineHeight: "1.7" }}>
              Revolutionizing sleep health through AI-driven ECG analytics. 
              Developed with passion for better healthcare diagnostics.
            </p>
          </Col>
          <Col md={4} className="text-md-center">
            <h6 className="text-white mb-3">Quick Links</h6>
            <ul className="list-unstyled" style={{ fontSize: "0.9rem" }}>
              <li className="mb-2"><Link to="/" className="text-decoration-none text-reset hover-primary">Home</Link></li>
              <li className="mb-2"><Link to="/analysis" className="text-decoration-none text-reset hover-primary">Analysis Port</Link></li>
              <li className="mb-2"><Link to="/about" className="text-decoration-none text-reset hover-primary">About the Team</Link></li>
            </ul>
          </Col>
          <Col md={4} className="text-md-end">
            <h6 className="text-white mb-3">Department</h6>
            <p className="mb-1" style={{ fontSize: "0.9rem" }}>Information Technology</p>
            <p className="mb-0" style={{ fontSize: "0.9rem" }}>GRIET, Hyderabad</p>
          </Col>
        </Row>
        <hr className="my-4" style={{ borderColor: "rgba(255,255,255,0.1)" }} />
        <Row>
          <Col className="text-center">
            <p className="mb-0" style={{ fontSize: "0.85rem" }}>
              © {currentYear} Sammith Reddy, Manish Reddy, Maruthi Reddy. All Rights Reserved.
            </p>
            <p className="mt-1" style={{ fontSize: "0.75rem", opacity: 0.5 }}>
              Major Project - IT Department - Gokaraju Rangaraju Institute of Engineering and Technology
            </p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
}

export default Footer;
