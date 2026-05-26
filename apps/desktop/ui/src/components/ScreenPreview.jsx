export default function ScreenPreview({ image }) {
  if (!image) return null;
  return <img src={image} alt="Screen Preview" width="100%" />;
}
