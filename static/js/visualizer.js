/**
 * Visualizer Module
 * Handles drawing pitch curves and waveform comparison graphs on canvas.
 */

function renderPitchChart(canvasId, refPitch = [], userPitch = []) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  // High-DPI Scaling
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);

  // Background Grid
  ctx.fillStyle = '#060910';
  ctx.fillRect(0, 0, width, height);

  ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
  ctx.lineWidth = 1;
  for (let y = 30; y < height; y += 30) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }

  if ((!refPitch || refPitch.length === 0) && (!userPitch || userPitch.length === 0)) return;

  // Find min & max F0 values
  const allVals = [...(refPitch || []), ...(userPitch || [])].filter(v => v > 0);
  const minF0 = allVals.length > 0 ? Math.min(...allVals) * 0.85 : 80;
  const maxF0 = allVals.length > 0 ? Math.max(...allVals) * 1.15 : 300;

  function getYCoordinate(f0Val) {
    if (f0Val <= 0) return height - 10;
    const norm = (f0Val - minF0) / (maxF0 - minF0);
    return height - (norm * (height - 30) + 15);
  }

  // 1. Draw Target Pitch Curve (Cyan)
  if (refPitch && refPitch.length > 0) {
    ctx.strokeStyle = '#06b6d4';
    ctx.lineWidth = 3;
    ctx.beginPath();
    
    const step = width / (refPitch.length - 1);
    refPitch.forEach((val, i) => {
      const x = i * step;
      const y = getYCoordinate(val);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  }

  // 2. Draw User Pitch Curve (Violet)
  if (userPitch && userPitch.length > 0) {
    ctx.strokeStyle = '#8b5cf6';
    ctx.lineWidth = 3;
    ctx.setLineDash([4, 4]); // Dashed line for user spoken pitch
    ctx.beginPath();

    const step = width / (userPitch.length - 1);
    userPitch.forEach((val, i) => {
      const x = i * step;
      const y = getYCoordinate(val);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.setLineDash([]); // Reset dash

    // Draw user pitch points
    ctx.fillStyle = '#a78bfa';
    userPitch.forEach((val, i) => {
      if (val > 0) {
        const x = i * step;
        const y = getYCoordinate(val);
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    });
  }
}


function animateScoreGauge(targetScore) {
  const circle = document.getElementById('gauge-fill-circle');
  const valText = document.getElementById('overall-score-val');
  if (!circle || !valText) return;

  const circumference = 326.7; // 2 * PI * 52
  const offset = circumference - (targetScore / 100) * circumference;
  
  circle.style.strokeDashoffset = offset;

  // Animate text number from 0 to targetScore
  let current = 0;
  const step = Math.max(1, Math.round(targetScore / 30));
  const interval = setInterval(() => {
    current += step;
    if (current >= targetScore) {
      current = targetScore;
      clearInterval(interval);
    }
    valText.textContent = current;
  }, 20);
}
