import React from "react";
import { Navbar, Container, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";

function AppNavbar() {
  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="py-3 sticky-top" style={{ backdropFilter: "blur(10px)", background: "rgba(33, 37, 41, 0.95)" }}>
      <Container>
        <Navbar.Brand as={Link} to="/" style={{ fontSize: "1.5rem", fontWeight: "800", color: "#fff", letterSpacing: "-0.5px" }}>
          <span style={{ color: "var(--primary)", marginRight: "8px" }}>🩺</span> 
          Apnea<span style={{ opacity: 0.8, fontWeight: 400 }}>Detect</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto align-items-center">
            <Nav.Link as={Link} to="/" className="px-3" style={{ fontSize: "1.05rem", fontWeight: "500", color: "rgba(255,255,255,0.85)", transition: "color 0.2s" }}>
              Home
            </Nav.Link>
            <Nav.Link as={Link} to="/analysis" className="px-3" style={{ fontSize: "1.05rem", fontWeight: "500", color: "rgba(255,255,255,0.85)", transition: "color 0.2s" }}>
              Analysis
            </Nav.Link>
            <Link to="/analysis" className="btn btn-primary btn-sm ms-3 px-4 py-2" style={{ borderRadius: "20px", fontWeight: "600" }}>
              Try Now
            </Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default AppNavbar;
