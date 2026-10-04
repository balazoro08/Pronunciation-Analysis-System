/**
 * AudioRecorder Module
 * Handles Web Audio API microphone stream, real-time visualizer canvas, and audio recording.
 */

class AudioRecorder {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.canvasCtx = this.canvas ? this.canvas.getContext('2d') : null;
    
    this.audioCtx = null;
    this.analyser = null;
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.recordedBlob = null;
    
    this.isRecording = false;
    this.animFrameId = null;
    this.startTime = 0;
    this.timerInterval = null;
    
    this.onStateChange = null;
  }

  async start() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const source = this.audioCtx.createMediaStreamSource(stream);
      
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 256;
      source.connect(this.analyser);

      // Determine supported mimeType
      let options = { mimeType: 'audio/webm' };
      if (!MediaRecorder.isTypeSupported('audio/webm')) {
        if (MediaRecorder.isTypeSupported('audio/mp4')) options = { mimeType: 'audio/mp4' };
        else options = {};
      }

      this.mediaRecorder = new MediaRecorder(stream, options);
      this.audioChunks = [];

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        const mimeType = this.mediaRecorder.mimeType || 'audio/webm';
        this.recordedBlob = new Blob(this.audioChunks, { type: mimeType });
        if (this.onStateChange) this.onStateChange('stopped', this.recordedBlob);
      };

      this.mediaRecorder.start(100);
      this.isRecording = true;
      this.startTime = Date.now();
      
      this.drawVisualizer();
      this.startTimer();
      
      if (this.onStateChange) this.onStateChange('recording');
    } catch (err) {
      console.error('Microphone access error:', err);
      alert('Microphone access was denied or is unavailable. Please check permissions.');
    }
  }

  stop() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.isRecording = false;
      
      if (this.mediaRecorder.stream) {
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
      }
      
      cancelAnimationFrame(this.animFrameId);
      clearInterval(this.timerInterval);
      
      // Clear visualizer
      if (this.canvasCtx) {
        this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      }
    }
  }

  startTimer() {
    const timerEl = document.getElementById('record-timer');
    this.timerInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
      const secs = String(elapsed % 60).padStart(2, '0');
      const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
      if (timerEl) timerEl.textContent = `${mins}:${secs}`;
    }, 200);
  }

  drawVisualizer() {
    if (!this.isRecording || !this.analyser || !this.canvasCtx) return;

    const bufferLength = this.analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    this.analyser.getByteFrequencyData(dataArray);

    const width = this.canvas.width;
    const height = this.canvas.height;

    this.canvasCtx.clearRect(0, 0, width, height);

    // Draw dark background grid lines
    this.canvasCtx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    this.canvasCtx.lineWidth = 1;
    this.canvasCtx.beginPath();
    this.canvasCtx.moveTo(0, height / 2);
    this.canvasCtx.lineTo(width, height / 2);
    this.canvasCtx.stroke();

    // Draw frequency bar spectrum
    const barWidth = (width / bufferLength) * 2.5;
    let x = 0;

    for (let i = 0; i < bufferLength; i++) {
      const barHeight = (dataArray[i] / 255) * height;

      // Gradient bars: Cyan to Emerald
      const gradient = this.canvasCtx.createLinearGradient(0, height, 0, height - barHeight);
      gradient.addColorStop(0, '#10b981');
      gradient.addColorStop(1, '#06b6d4');

      this.canvasCtx.fillStyle = gradient;
      this.canvasCtx.fillRect(x, height - barHeight, barWidth - 1, barHeight);

      x += barWidth;
    }

    this.animFrameId = requestAnimationFrame(() => this.drawVisualizer());
  }
}
