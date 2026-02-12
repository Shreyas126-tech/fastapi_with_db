import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const navigate = useNavigate();
    const [history, setHistory] = useState([]);
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (!token) {
            navigate("/");
            return;
        }
        fetchHistory();
    }, [navigate]);

    const fetchHistory = async () => {
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("http://localhost:8000/history", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (res.ok) {
                const data = await res.json();
                setHistory(data);
            }
        } catch (error) {
            console.error("Error fetching history:", error);
        }
    };

    const handleAsk = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        setLoading(true);
        setResponse("");
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("http://localhost:8000/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ message }),
            });

            if (res.ok) {
                const data = await res.json();
                setResponse(data.response);
                setMessage("");
                fetchHistory(); // Refresh history
            } else {
                alert("Failed to get response from AI");
            }
        } catch (error) {
            console.error("Error asking AI:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.sidebar}>
                <h2 style={styles.sidebarTitle}>History</h2>
                <div style={styles.historyList}>
                    {history.length === 0 ? (
                        <p style={styles.noHistory}>No history yet</p>
                    ) : (
                        history.map((item) => (
                            <div key={item.id} style={styles.historyItem}>
                                <p style={styles.historyPrompt}>{item.prompt}</p>
                                <p style={styles.historyTime}>
                                    {new Date(item.timestamp).toLocaleString()}
                                </p>
                            </div>
                        ))
                    )}
                </div>
                <button
                    onClick={() => { localStorage.removeItem("access_token"); navigate("/"); }}
                    style={styles.logoutBtn}
                >
                    Logout
                </button>
            </div>

            <div style={styles.mainContent}>
                <header style={styles.header}>
                    <h1>AI Assistant Dashboard 🎉</h1>
                </header>

                <div style={styles.chatArea}>
                    {response && (
                        <div style={styles.responseBox}>
                            <strong>AI:</strong>
                            <p>{response}</p>
                        </div>
                    )}
                </div>

                <form onSubmit={handleAsk} style={styles.inputContainer}>
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Type your prompt here..."
                        style={styles.input}
                        disabled={loading}
                    />
                    <button type="submit" style={styles.sendBtn} disabled={loading}>
                        {loading ? "Thinking..." : "Send"}
                    </button>
                </form>
            </div>
        </div>
    );
}

const styles = {
    container: {
        display: "flex",
        height: "100vh",
        fontFamily: "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        backgroundColor: "#0f172a",
        color: "#f8fafc",
    },
    sidebar: {
        width: "300px",
        backgroundColor: "#1e293b",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        borderRight: "1px solid #334155",
    },
    sidebarTitle: {
        fontSize: "1.5rem",
        marginBottom: "20px",
        color: "#38bdf8",
    },
    historyList: {
        flex: 1,
        overflowY: "auto",
        marginBottom: "20px",
    },
    historyItem: {
        padding: "10px",
        borderRadius: "8px",
        backgroundColor: "#334155",
        marginBottom: "10px",
        cursor: "pointer",
        transition: "background-color 0.2s",
    },
    historyPrompt: {
        margin: 0,
        fontSize: "0.9rem",
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
    },
    historyTime: {
        margin: "5px 0 0 0",
        fontSize: "0.7rem",
        color: "#94a3b8",
    },
    noHistory: {
        textAlign: "center",
        color: "#94a3b8",
        fontSize: "0.9rem",
    },
    logoutBtn: {
        padding: "10px",
        backgroundColor: "#ef4444",
        color: "white",
        border: "none",
        borderRadius: "8px",
        cursor: "pointer",
        fontWeight: "bold",
    },
    mainContent: {
        flex: 1,
        display: "flex",
        flexDirection: "column",
        padding: "40px",
        backgroundImage: "radial-gradient(circle at top right, #1e293b, #0f172a)",
    },
    header: {
        marginBottom: "40px",
        textAlign: "center",
    },
    chatArea: {
        flex: 1,
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
        gap: "20px",
        padding: "20px",
    },
    responseBox: {
        backgroundColor: "rgba(255, 255, 255, 0.05)",
        backdropFilter: "blur(10px)",
        padding: "20px",
        borderRadius: "15px",
        border: "1px solid rgba(255, 255, 255, 0.1)",
        maxWidth: "80%",
        lineHeight: "1.6",
    },
    inputContainer: {
        display: "flex",
        gap: "10px",
        marginTop: "20px",
    },
    input: {
        flex: 1,
        padding: "15px",
        borderRadius: "10px",
        border: "1px solid #475569",
        backgroundColor: "#1e293b",
        color: "white",
        fontSize: "1rem",
        outline: "none",
    },
    sendBtn: {
        padding: "0 30px",
        backgroundColor: "#0ea5e9",
        color: "white",
        border: "none",
        borderRadius: "10px",
        cursor: "pointer",
        fontWeight: "bold",
        transition: "background-color 0.2s",
    },
};

export default Dashboard;
