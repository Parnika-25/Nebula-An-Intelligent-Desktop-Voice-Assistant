export default function CommandLog({ logs = [] }) {
  return (
    <ul>
      {logs.map((log, i) => (
        <li key={i}>{log}</li>
      ))}
    </ul>
  );
}
