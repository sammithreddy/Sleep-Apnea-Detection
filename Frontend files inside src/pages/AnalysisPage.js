import React from "react";
import UploadECG from "../components/UploadECG";

function AnalysisPage() {
  return (
    <div className="container mt-4">
      <h2 className="text-center">ECG Analysis</h2>
      <UploadECG />
    </div>
  );
}

export default AnalysisPage;
