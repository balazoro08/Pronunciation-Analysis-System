/**
 * Main App Controller
 * Integrates catalog loading, TTS synthesis, recording events, API fetch, and score display.
 */

document.addEventListener('DOMContentLoaded', () => {
  // App State
  let currentLang = 'en';
  let catalog = [];
  let selectedWord = null;
  let recordedBlob = null;
  let attemptCount = 0;

  // DOM Elements
  const btnLangEn = document.getElementById('btn-lang-en');
  const btnLangJa = document.getElementById('btn-lang-ja');
  const activeLangBadge = document.getElementById('active-lang-badge');
  
  const wordSelect = document.getElementById('word-select');
  const btnListenNative = document.getElementById('btn-listen-native');
  const customWordWrapper = document.getElementById('custom-word-wrapper');
  const customWordInput = document.getElementById('custom-word-input');

  const displayTargetWord = document.getElementById('display-target-word');
  const displayIpa = document.getElementById('display-ipa');
  const displayCategory = document.getElementById('display-category');
  const displayDifficulty = document.getElementById('display-difficulty');
  const displayPitchProfile = document.getElementById('display-pitch-profile');
  const displayTip = document.getElementById('display-tip');

  const btnRecord = document.getElementById('btn-record');
  const recordBtnText = document.getElementById('record-btn-text');
  const recordStatus = document.getElementById('record-status');
  const btnPlaySpoken = document.getElementById('btn-play-spoken');
  const btnAnalyze = document.getElementById('btn-analyze');

  const idleResultsState = document.getElementById('idle-results-state');
  const analysisOutputState = document.getElementById('analysis-output-state');
  
  const gradeBadge = document.getElementById('grade-badge');
  const gradeTitle = document.getElementById('grade-title');
  const gradeDescription = document.getElementById('grade-description');
  const spokenTranscript = document.getElementById('spoken-transcript');

  const scorePhonetic = document.getElementById('score-phonetic');
  const scorePitch = document.getElementById('score-pitch');
  const scoreFluency = document.getElementById('score-fluency');
  const scoreClarity = document.getElementById('score-clarity');
  
  const barPhonetic = document.getElementById('bar-phonetic');
  const barPitch = document.getElementById('bar-pitch');
  const barFluency = document.getElementById('bar-fluency');
  const barClarity = document.getElementById('bar-clarity');

  const phonemeCardsList = document.getElementById('phoneme-cards-list');
  const feedbackTipsList = document.getElementById('feedback-tips-list');
  const attemptCountEl = document.getElementById('attempt-count');

  // Initialize Recorder instance
  const recorder = new AudioRecorder('live-audio-canvas');

  recorder.onStateChange = (state, blob) => {
    if (state === 'recording') {
      btnRecord.classList.add('recording');
      recordBtnText.textContent = 'Stop Recording';
      recordStatus.textContent = '🎙️ Recording spoken audio... Speak clearly!';
      btnAnalyze.disabled = true;
      btnPlaySpoken.disabled = true;
    } else if (state === 'stopped') {
      btnRecord.classList.remove('recording');
      recordBtnText.textContent = 'Re-record Spoken';
      recordStatus.textContent = '✅ Recording finished. Ready for analysis!';
      recordedBlob = blob;
      btnPlaySpoken.disabled = false;
      btnAnalyze.disabled = false;
    }
  };

  // 1. Language Toggle Listeners
  btnLangEn.addEventListener('click', () => switchLanguage('en'));
  btnLangJa.addEventListener('click', () => switchLanguage('ja'));

  function switchLanguage(lang) {
    currentLang = lang;
    if (lang === 'en') {
      btnLangEn.classList.add('active');
      btnLangJa.classList.remove('active');
      activeLangBadge.textContent = 'English Mode';
    } else {
      btnLangJa.classList.add('active');
      btnLangEn.classList.remove('active');
      activeLangBadge.textContent = '日本語 Mode';
    }
    loadCatalog(lang);
  }

  // 2. Fetch Catalog from Backend
  async function loadCatalog(lang) {
    try {
      const res = await fetch(`/api/catalog?lang=${lang}`);
      const data = await res.json();
      catalog = data.words || [];
      populateWordSelect();
    } catch (err) {
      console.error('Failed to load catalog:', err);
    }
  }

  function populateWordSelect() {
    wordSelect.innerHTML = '';
    
    catalog.forEach(item => {
      const opt = document.createElement('option');
      opt.value = item.id;
      opt.textContent = `${item.word} (${item.category})`;
      wordSelect.appendChild(opt);
    });

    // Option for custom word
    const customOpt = document.createElement('option');
    customOpt.value = 'custom';
    customOpt.textContent = '✏️ Custom Word / Phrase...';
    wordSelect.appendChild(customOpt);

    if (catalog.length > 0) {
      wordSelect.value = catalog[0].id;
      onWordSelected(catalog[0].id);
    }
  }

  wordSelect.addEventListener('change', (e) => onWordSelected(e.target.value));

  function onWordSelected(id) {
    if (id === 'custom') {
      customWordWrapper.style.display = 'flex';
      selectedWord = {
        id: 'custom',
        word: customWordInput.value || 'Custom Word',
        language: currentLang,
        ipa: '/custom/',
        category: 'Custom Practice',
        difficulty: 'Flexible',
        pitch_pattern: 'H-L',
        tip: 'Practice your own custom word or phrase.'
      };
    } else {
      customWordWrapper.style.display = 'none';
      selectedWord = catalog.find(item => item.id === id);
    }
    updateTargetWordCard();
  }

  customWordInput.addEventListener('input', () => {
    if (wordSelect.value === 'custom') {
      selectedWord.word = customWordInput.value || 'Custom Word';
      displayTargetWord.textContent = selectedWord.word;
    }
  });

  function updateTargetWordCard() {
    if (!selectedWord) return;
    displayTargetWord.textContent = selectedWord.word;
    displayIpa.textContent = selectedWord.ipa || selectedWord.romaji || '';
    displayCategory.textContent = selectedWord.category || 'General';
    displayDifficulty.textContent = selectedWord.difficulty || 'Normal';
    displayPitchProfile.textContent = `Pitch: ${selectedWord.pitch_pattern || selectedWord.pitch_profile || 'Normal'}`;
    displayTip.innerHTML = `<i class="fa-solid fa-lightbulb"></i> ${selectedWord.tip || 'Speak clearly at normal conversational speed.'}`;
  }

  // 3. Native Text-to-Speech Playback
  btnListenNative.addEventListener('click', () => {
    if (!selectedWord) return;
    const textToSpeak = selectedWord.word.split(' (')[0];
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = currentLang === 'ja' ? 'ja-JP' : 'en-US';
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  });

  // 4. Recording Controls
  btnRecord.addEventListener('click', () => {
    if (recorder.isRecording) {
      recorder.stop();
    } else {
      recorder.start();
    }
  });

  btnPlaySpoken.addEventListener('click', () => {
    if (recordedBlob) {
      const audioUrl = URL.createObjectURL(recordedBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    }
  });

  // 5. Submit Audio for Pronunciation Analysis
  btnAnalyze.addEventListener('click', async () => {
    if (!recordedBlob || !selectedWord) return;

    btnAnalyze.disabled = true;
    btnAnalyze.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...`;

    const formData = new FormData();
    formData.append('audio', recordedBlob, 'spoken_recording.webm');
    formData.append('target_word', selectedWord.word);
    formData.append('language', currentLang);
    if (selectedWord.id !== 'custom') {
      formData.append('word_id', selectedWord.id);
    }

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();

      if (data.success) {
        attemptCount++;
        attemptCountEl.textContent = attemptCount;
        renderAnalysisResults(data);
      } else {
        alert('Analysis Error: ' + (data.error || 'Unknown error occurred'));
      }
    } catch (err) {
      console.error('API analyze error:', err);
      alert('Failed to connect to analysis server.');
    } finally {
      btnAnalyze.disabled = false;
      btnAnalyze.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze Pronunciation`;
    }
  });

  // 6. Render Results UI
  function renderAnalysisResults(data) {
    idleResultsState.classList.add('hidden');
    analysisOutputState.classList.remove('hidden');

    // Score Hero & Gauge
    animateScoreGauge(data.overall_score);
    gradeBadge.textContent = `${data.grade} Grade`;
    gradeTitle.textContent = data.grade_label;
    gradeDescription.textContent = `Acoustic Duration: ${data.acoustic.duration_sec}s | Mean Pitch: ${data.acoustic.mean_f0_hz} Hz`;
    spokenTranscript.textContent = `"${data.recognized_text}"`;

    // Category Metric Bars
    const m = data.metrics;
    scorePhonetic.textContent = `${m.phonetic_score}%`;
    scorePitch.textContent = `${m.pitch_score}%`;
    scoreFluency.textContent = `${m.fluency_score}%`;
    scoreClarity.textContent = `${m.clarity_score}%`;

    barPhonetic.style.width = `${m.phonetic_score}%`;
    barPitch.style.width = `${m.pitch_score}%`;
    barFluency.style.width = `${m.fluency_score}%`;
    barClarity.style.width = `${m.clarity_score}%`;

    // Phoneme Diagnostic Cards
    phonemeCardsList.innerHTML = '';
    if (data.phonetic_breakdown && data.phonetic_breakdown.length > 0) {
      data.phonetic_breakdown.forEach(item => {
        const card = document.createElement('div');
        card.className = `phoneme-card status-${item.status}`;
        card.innerHTML = `
          <span class="target-p">${item.target_phoneme}</span>
          <span class="spoken-p">${item.spoken_phoneme}</span>
          <span class="p-label">${item.label}</span>
        `;
        phonemeCardsList.appendChild(card);
      });
    }

    // Pitch Contour Overlay Canvas
    renderPitchChart('pitch-contour-canvas', data.acoustic.ref_pitch_curve, data.acoustic.user_pitch_curve);

    // Feedback Tips List
    feedbackTipsList.innerHTML = '';
    if (data.feedback && data.feedback.length > 0) {
      data.feedback.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        feedbackTipsList.appendChild(li);
      });
    }
  }

  // Load initial catalog
  loadCatalog('en');
});
