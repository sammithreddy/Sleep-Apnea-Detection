import React from "react";
import { Bar, Pie } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from "chart.js";

// Register required chart components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function SleepApneaStats() {
  // 🌎 Global Sleep Apnea Prevalence (Pie Chart)
  const globalPrevalenceData = {
    labels: ["People with Sleep Apnea", "People without Sleep Apnea"],
    datasets: [
      {
        label: "Prevalence(in millions)",
        data: [936, 7064], // 936M have it, 7.064B don't
        backgroundColor: ["#ff6384", "#36a2eb"],
        hoverOffset: 4,
      },
    ],
  };

  // 🧑‍⚕️ Sleep Apnea Cases by Age & Gender (Bar Chart)
  const ageGenderData = {
    labels: ["18-30", "31-45", "46-60", "60+"],
    datasets: [
      {
        label: "Men%",
        data: [8, 12, 22, 30], // % of men affected by age
        backgroundColor: "#36a2eb",
      },
      {
        label: "Women%",
        data: [4, 8, 16, 25], // % of women affected by age
        backgroundColor: "#ff6384",
      },
    ],
  };

  // 📍 Untreated vs Diagnosed Cases (Pie Chart)
  const diagnosisData = {
    labels: ["Diagnosed Cases", "Undiagnosed Cases"],
    datasets: [
      {
        label: "Diagnosis Rate(%)",
        data: [20, 80], // 80% remain undiagnosed
        backgroundColor: ["#ffce56", "#ff6384"],
        hoverOffset: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  return (
    <div className="mt-5 pt-4 animate-fade-in">
      <h3 className="text-center mb-5" style={{ fontWeight: "700", color: "var(--dark)" }}>🌍 Global Sleep Apnea Statistics</h3>

      <div className="d-flex justify-content-center flex-wrap">
        {/* Pie Chart: Global Prevalence */}
        <div style={{ width: "300px", margin: "20px" }}>
          <h6 className="text-center">Global Prevalence</h6>
          <Pie data={globalPrevalenceData} />
        </div>

        {/* Bar Chart: Age & Gender Breakdown */}
        <div style={{ width: "500px", margin: "20px" }}>
          <h6 className="text-center">Age & Gender Distribution</h6>
          <Bar data={ageGenderData} options={options} />
        </div>

        {/* Pie Chart: Diagnosed vs Undiagnosed Cases */}
        <div style={{ width: "300px", margin: "20px" }}>
          <h6 className="text-center">Undiagnosed vs Diagnosed</h6>
          <Pie data={diagnosisData} />
        </div>
      </div>
    </div>
  );
}

export default SleepApneaStats;
