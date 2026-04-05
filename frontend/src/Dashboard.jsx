import React, { useEffect, useState } from "react";
import {
  getSummary,
  getTrends,
  getRecords,
  createRecord,
  deleteRecord,
} from "./api";

const Dashboard = ({ setLoggedIn }) => {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState([]);
  const [records, setRecords] = useState([]);

  const [amount, setAmount] = useState("");
  const [type, setType] = useState("income");

  const fetchData = async () => {
    try {
      const summaryRes = await getSummary();
      const trendsRes = await getTrends();
      const recordsRes = await getRecords();

      // ===== SUMMARY =====
      const summaryData = summaryRes.data;
      setSummary(summaryData);

      // ===== TRENDS (handle all formats) =====
      const trendsData = trendsRes.data;
      if (Array.isArray(trendsData)) {
        setTrends(trendsData);
      } else if (Array.isArray(trendsData.data)) {
        setTrends(trendsData.data);
      } else if (Array.isArray(trendsData.trends)) {
        setTrends(trendsData.trends);
      } else {
        setTrends([]);
      }

      // ===== RECORDS (handle pagination) =====
      const recordsData = recordsRes.data;
      if (Array.isArray(recordsData)) {
        setRecords(recordsData);
      } else if (Array.isArray(recordsData.results)) {
        setRecords(recordsData.results);
      } else {
        setRecords([]);
      }

      // DEBUG (you can remove later)
      console.log("SUMMARY:", summaryData);
      console.log("TRENDS:", trendsData);
      console.log("RECORDS:", recordsData);

    } catch (err) {
      alert("Error loading dashboard");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const addRecord = async () => {
    try {
      await createRecord({
        amount,
        record_type: type,
        category: "other",
        date: "2026-01-01",
      });

      setAmount("");
      fetchData();
    } catch (err) {
      alert("Error creating record");
    }
  };

  const handleDelete = async (id) => {
    await deleteRecord(id);
    fetchData();
  };

  const logout = () => {
    localStorage.clear();
    setLoggedIn(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Dashboard</h1>

      <button onClick={logout}>Logout</button>

      {/* ===== CARDS ===== */}
      <div style={{ display: "flex", gap: 20, marginTop: 20 }}>
        
        {/* SUMMARY CARD */}
        <div style={{ border: "1px solid black", padding: 20, width: "50%" }}>
          <h3>Summary</h3>

          {summary ? (
            <>
              <p>
                Total Income: ₹
                {summary.total_income || summary.income || 0}
              </p>

              <p>
                Total Expense: ₹
                {summary.total_expense || summary.expense || 0}
              </p>

              <p>
                Balance: ₹
                {summary.balance !== undefined
                  ? summary.balance
                  : (summary.total_income || summary.income || 0) -
                    (summary.total_expense || summary.expense || 0)}
              </p>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>

        {/* TRENDS CARD */}
        <div style={{ border: "1px solid black", padding: 20, width: "50%" }}>
          <h3>Trends</h3>

          {trends.length > 0 ? (
            trends.map((t, index) => (
              <div key={index}>
                <p>
                  {(t.date || t.month || "N/A")} → ₹
                  {(t.total || t.amount || 0)}
                </p>
              </div>
            ))
          ) : (
            <p>No trends data</p>
          )}
        </div>
      </div>

      {/* ===== ADD RECORD ===== */}
      <h3 style={{ marginTop: 30 }}>Add Record</h3>

      <input
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />

      <select onChange={(e) => setType(e.target.value)}>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>

      <button onClick={addRecord}>Add</button>

      {/* ===== RECORDS ===== */}
      <h3 style={{ marginTop: 30 }}>Records</h3>

      {records.length > 0 ? (
        records.map((r) => (
          <div
            key={r.id}
            style={{ border: "1px solid gray", margin: 10, padding: 10 }}
          >
            <p>
              {r.record_type} - ₹{r.amount}
            </p>
            <button onClick={() => handleDelete(r.id)}>Delete</button>
          </div>
        ))
      ) : (
        <p>No records found</p>
      )}
    </div>
  );
};

export default Dashboard;