const STORAGE = {
  quizScore: 'cyberguard.quizScore',
  safetyScore: 'cyberguard.safetyScore',
  notifications: 'cyberguard.notifications',
  reduceMotion: 'cyberguard.reduceMotion',
  theme: 'cyberguard.theme',
  notificationsRead: 'cyberguard.notificationsRead',
  plan: 'cyberguard.plan',
  chat: 'cyberguard.chat'
};

const readNumber = (key, fallback) => {
  const value = Number(localStorage.getItem(key));
  return Number.isFinite(value) && value >= 0 ? value : fallback;
};
const savedQuizScore = () => localStorage.getItem(STORAGE.quizScore);
let safetyScore = readNumber(STORAGE.safetyScore, 82);
let activeContentType = 'Email';
let toastTimer;

const quizQuestions = [
  { topic: 'PHISHING AWARENESS', question: 'A message says your bank account will be blocked unless you click a link. What should you do?', options: ['Click immediately', 'Reply with your account details', 'Verify through the official bank app or website', 'Forward it to friends'], answer: 2, explanation: 'Urgency is a common pressure tactic. Contact the bank through a channel you already trust.' },
  { topic: 'PASSWORD SECURITY', question: 'Which password habit best protects your accounts?', options: ['Reuse one memorable password', 'Use a long, unique password for every account', 'Add your birth year to a familiar word', 'Change one character in the same password'], answer: 1, explanation: 'Unique passwords keep a breach at one service from unlocking other accounts.' },
  { topic: 'MULTI-FACTOR AUTHENTICATION', question: 'A login approval appears on your phone, but you are not signing in. What should you do?', options: ['Approve it to clear the alert', 'Deny it and secure your account', 'Share the code with the caller', 'Turn off account alerts'], answer: 1, explanation: 'An unexpected approval may mean someone has your password. Deny it and review account activity.' },
  { topic: 'SAFE BROWSING', question: 'A shopping website has a misspelled version of the store’s name in its address. What is safest?', options: ['Continue if it looks professional', 'Enter payment details to test it', 'Use a trusted bookmark or official app', 'Trust it because it has a padlock'], answer: 2, explanation: 'Scam sites can copy a brand’s design. Check the exact domain and use a known route.' },
  { topic: 'SOCIAL ENGINEERING', question: 'Someone claiming to be IT asks for your password to fix an issue. How do you respond?', options: ['Send it if they know your name', 'Ask them to send you a login code', 'Refuse and contact IT through a verified channel', 'Share it and change it later'], answer: 2, explanation: 'Legitimate support staff should not need your password or one-time codes.' },
  { topic: 'TEXT MESSAGE SAFETY', question: 'A delivery text asks you to pay a small fee at an unfamiliar link. What should you do?', options: ['Pay quickly so delivery is not delayed', 'Open the carrier’s official app to check', 'Reply with your address', 'Forward the link to a friend'], answer: 1, explanation: 'Check deliveries through the official carrier app or website, not an unexpected text link.' },
  { topic: 'PASSWORD MANAGERS', question: 'What is a password manager mainly useful for?', options: ['Reusing one password safely', 'Creating and storing unique passwords', 'Removing the need for device updates', 'Sharing passwords by email'], answer: 1, explanation: 'A reputable password manager helps generate and store a different strong password for each account.' },
  { topic: 'PUBLIC WI-FI', question: 'You need to access your bank while connected to public Wi-Fi. What is best?', options: ['Use a link sent by text', 'Wait or use the bank’s official app on a trusted connection', 'Disable your screen lock', 'Use any site with a padlock'], answer: 1, explanation: 'Use the official app or a trusted connection, and avoid links received in messages.' },
  { topic: 'ONE-TIME CODES', question: 'A caller asks you to read them a verification code. What should you do?', options: ['Share it if they know your name', 'Share only the first half', 'Never share it; end the call and verify independently', 'Send it by text instead'], answer: 2, explanation: 'One-time codes are meant for you. A legitimate support agent should not ask you to reveal them.' },
  { topic: 'SOFTWARE UPDATES', question: 'Your phone offers an operating-system security update. What should you do?', options: ['Install it from system settings when practical', 'Ignore it until the phone stops working', 'Install an update file from a pop-up ad', 'Turn off automatic updates'], answer: 0, explanation: 'Updates often fix known security flaws. Install them through the device’s official settings.' },
  { topic: 'EMAIL ATTACHMENTS', question: 'An unexpected invoice arrives as an attachment. What is safest?', options: ['Open it to identify the sender', 'Enable macros if prompted', 'Verify with the sender through a known channel', 'Forward it to your contacts'], answer: 2, explanation: 'Unexpected attachments can be harmful. Verify the request independently before opening.' },
  { topic: 'APP PERMISSIONS', question: 'A flashlight app requests access to your contacts and microphone. What should you do?', options: ['Allow everything to continue', 'Deny permissions it does not need', 'Share your contacts first', 'Disable your phone lock'], answer: 1, explanation: 'Grant only permissions needed for an app’s function, and review them periodically.' },
  { topic: 'PAYMENT SCAMS', question: 'A seller insists you pay with gift cards to reserve an item. What should you do?', options: ['Pay quickly to secure the deal', 'Use a protected payment method or walk away', 'Send the card code only', 'Share your banking password'], answer: 1, explanation: 'Gift cards are difficult to recover and are not a normal protected payment method for purchases.' },
  { topic: 'PRIVACY SETTINGS', question: 'A social profile is public by default. What is a useful first step?', options: ['Post your travel dates', 'Review visibility and limit personal details', 'Reuse your email password', 'Accept every follow request'], answer: 1, explanation: 'Limit who can see personal details and review privacy settings regularly.' },
  { topic: 'QR CODE SAFETY', question: 'A QR code on a public notice leads to a sign-in page. What should you do?', options: ['Enter your password immediately', 'Check the destination and navigate to the service directly', 'Approve any browser warning', 'Share the code with coworkers'], answer: 1, explanation: 'QR codes can hide destinations. Check the address and use the service’s known official website.' },
  { topic: 'ACCOUNT RECOVERY', question: 'You receive an alert that your recovery email was changed, but you did not change it. What now?', options: ['Ignore it', 'Use the official site to secure the account and review sessions', 'Reply with your password', 'Click a link in a follow-up message'], answer: 1, explanation: 'Use a trusted route to regain control, change credentials, and review active sessions and recovery settings.' },
  { topic: 'BACKUPS', question: 'Why keep a separate backup of important files?', options: ['It prevents every phishing email', 'It helps restore files after loss or ransomware', 'It replaces software updates', 'It makes passwords public'], answer: 1, explanation: 'A separate, current backup can help restore information after device failure or an attack.' },
  { topic: 'LOGIN LINKS', question: 'A message asks you to scan a QR code to keep your work account active. What is safest?', options: ['Scan and sign in immediately', 'Open the work service from a saved bookmark', 'Send your password to IT', 'Approve any MFA request'], answer: 1, explanation: 'Use a known bookmark or official app instead of an unexpected sign-in link or QR code.' },
  { topic: 'IMPERSONATION', question: 'A familiar voice urgently asks you to transfer money. What should you do?', options: ['Transfer it immediately', 'Verify by calling a known number or using a separate channel', 'Ask them to text a code', 'Post about the request publicly'], answer: 1, explanation: 'Voices can be imitated. Verify unusual requests using a contact method you already trust.' },
  { topic: 'LOST DEVICES', question: 'A work phone is missing. What should you do first?', options: ['Wait a few days', 'Report it to your organization and use its device-lock process', 'Post account recovery codes online', 'Disable account alerts'], answer: 1, explanation: 'Prompt reporting lets your organization lock or locate the device and protect accounts.' }
];
const assessmentCount = 20;
const questionsPerAssessment = 5;

const learningGuides = [
  { title: 'Password Security', icon: 'key-round', tag: 'ACCOUNT BASICS', short: 'Build strong, unique passwords without the guesswork.', body: ['A strong password should be long, unique to one account, and difficult for someone else to guess. Avoid personal facts and common phrases, and never reuse your email password on other sites.', 'A password manager can generate and store distinct passwords so you do not have to memorize them all. Add multi-factor authentication to important accounts for another layer of protection.'], references: [['NIST Digital Identity Guidelines: Authentication', 'https://pages.nist.gov/800-63-4/sp800-63b.html']], tip: 'Start with your email account: update its password and turn on multi-factor authentication.' },
  { title: 'Phishing', icon: 'fish', tag: 'SCAM SPOTTING', short: 'Recognize messages designed to rush or trick you.', body: ['Phishing messages impersonate trusted organizations to make you click a link, open a file, or reveal private information. Watch for unexpected urgency, generic greetings, unusual payment requests, and sender addresses or domains that do not match.', 'Do not use the message’s link or phone number to verify a claim. Open the official app or type a known website address yourself, then report and delete messages that appear fraudulent.'], references: [['FTC: How To Recognize and Avoid Phishing Scams', 'https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams']], tip: 'Open the official app or type a known website address instead of following a message link.' },
  { title: 'Mobile Security', icon: 'smartphone', tag: 'DEVICE SAFETY', short: 'Protect the phone that holds so much of your life.', body: ['Your phone contains messages, accounts, photos, and location data. Keep its operating system and apps updated, use a screen lock, and install apps only from trusted stores.', 'Review permissions and remove apps you no longer use. If a message asks you to install an app or profile, verify the request through the provider’s official website or support channel first.'], references: [['FTC: How To Protect Your Phone From Hackers', 'https://consumer.ftc.gov/articles/how-protect-your-phone-hackers']], tip: 'Enable automatic updates and remove apps you no longer use.' },
  { title: 'Online Payments', icon: 'credit-card', tag: 'MONEY & SHOPPING', short: 'Shop and pay with fewer surprises.', body: ['Before buying, check the exact website address, research unfamiliar sellers, and read the delivery and refund terms. A padlock or HTTPS means a connection is encrypted; it does not prove that a seller is legitimate.', 'Prefer payment methods with dispute protections. Avoid sellers who insist on gift cards, wire transfers, or cryptocurrency, and keep receipts and order confirmations in case something goes wrong.'], references: [['FTC: Online Shopping', 'https://consumer.ftc.gov/articles/online-shopping']], tip: 'Turn on transaction alerts so unfamiliar charges are easier to catch.' },
  { title: 'Social Engineering', icon: 'users-round', tag: 'HUMAN FACTORS', short: 'Spot manipulation before it becomes a security problem.', body: ['Social engineering uses trust, authority, fear, or curiosity to pressure someone into sharing information or taking an unsafe action. A caller may impersonate a colleague, support agent, or family member, and caller ID can be faked.', 'Pause when a request is unexpected or urgent. Verify it using a separate contact method you already trust, and never share passwords or one-time codes with someone who contacts you.'], references: [['FTC: How To Spot, Avoid, and Report Tech Support Scams', 'https://consumer.ftc.gov/articles/how-spot-avoid-and-report-tech-support-scams']], tip: 'Pause and verify unusual requests using a separate, trusted communication channel.' },
  { title: 'Malware', icon: 'bug', tag: 'DEVICE SAFETY', short: 'Understand harmful software and how it gets installed.', body: ['Malware is software that can steal information, disrupt a device, or lock files. It may arrive through deceptive links, unexpected attachments, fake security warnings, or downloads from untrusted sites.', 'Keep security software and devices updated, download programs from sources you trust, and avoid opening unexpected files. If you suspect infection, stop using the device for sensitive logins, run a trusted security scan, and get help from a known support provider.'], references: [['FTC: Malware: How To Protect Against, Detect, and Remove It', 'https://consumer.ftc.gov/articles/malware-how-protect-against-detect-and-remove-it']], tip: 'Do not install software from pop-up warnings or unsolicited messages.' },
  { title: 'Privacy', icon: 'eye-off', tag: 'PERSONAL DATA', short: 'Share less and take control of your digital footprint.', body: ['Websites and apps may collect details such as your location, contacts, and browsing activity. Review privacy settings and permissions, and share only information needed for the service.', 'Think carefully before posting information that could reveal where you live, when you are away, or answers to account recovery questions. Check what data an app collects before installing it, and remove access that is no longer needed.'], references: [['FTC: Protect Your Personal Information and Data', 'https://consumer.ftc.gov/articles/protect-your-personal-information-and-data']], tip: 'Review location and microphone permissions for your apps today.' },
  { title: 'AI-related Scams', icon: 'bot', tag: 'EMERGING THREATS', short: 'Stay skeptical of convincing voices, images, and messages.', body: ['AI tools can help scammers create convincing messages or imitate a familiar voice. A familiar-sounding caller or personal detail is not proof of identity, especially when the request involves money or sensitive information.', 'Pause and contact the person using a number you already know or another trusted channel. Families and teams can agree on a verification phrase, and suspicious requests should be reported to the relevant service or authorities.'], references: [['FTC: Scammers Use AI to Enhance Their Family Emergency Schemes', 'https://consumer.ftc.gov/consumer-alerts/2023/03/scammers-use-ai-enhance-their-family-emergency-schemes']], tip: 'Use a family or team verification phrase for urgent requests involving money.' }
];

const chatApi = {
  async sendMessage(message) {
    if (window.cyberguardSetTrigger) {
      window.cyberguardSetTrigger('question', message);
      return null;
    }
    return mockAssistantReply(message);
  }
};

function mockAssistantReply(message) {
  const text = message.toLowerCase();
  if (/(email|phish|message|link|sms|text|scam)/.test(text)) {
    return 'Good instinct to check first. Look for an unexpected request, pressure to act, a sender or domain that does not quite match, and links asking for a sign-in. Avoid clicking; open the organization’s official app or site directly. You can paste the message into the Phishing Detector for a quick pattern check.';
  }
  if (/(password|passphrase|credential|login)/.test(text)) {
    return 'Use a long, unique password for every account. A password manager can create and remember them for you. Turn on multi-factor authentication for important accounts, and never share a password or one-time sign-in code.';
  }
  if (/(clicked|click|download|attachment|opened)/.test(text)) {
    return 'First, don’t panic. Close the page and don’t enter any information. If you entered a password, change it from the official website on a trusted device and enable multi-factor authentication. If you downloaded a file or entered payment details, contact your organization or bank through a verified channel.';
  }
  if (/(mfa|2fa|authenticat|verification code)/.test(text)) {
    return 'Multi-factor authentication adds a second check beyond your password. Prefer an authenticator app or security key when available. Never approve a login you did not start, and never share a one-time code with someone who contacts you.';
  }
  return 'A good security habit is to pause, verify, and use a trusted route. Don’t share passwords, one-time codes, or sensitive personal details. Tell me what happened (without private information), and I’ll help you think through a safe next step.';
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}
function formatAssistantContent(message) {
  const lines = String(message)
    .replace(/\r\n?/g, '\n')
    .replace(/\s+(?=\d+[.)]\s)/g, '\n')
    .split('\n');
  const blocks = [];
  let listType = '';
  let listItems = [];

  const formatInline = value => escapeHtml(value).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  const flushList = () => {
    if (listItems.length) blocks.push(`<${listType}>${listItems.map(item => `<li>${formatInline(item)}</li>`).join('')}</${listType}>`);
    listType = '';
    listItems = [];
  };

  lines.forEach(line => {
    const item = line.match(/^\s*(?:([-*•])\s+|(\d+)[.)]\s+)(.+)$/);
    if (item) {
      const nextType = item[2] ? 'ol' : 'ul';
      if (listType && listType !== nextType) flushList();
      listType = nextType;
      listItems.push(item[3]);
    } else {
      flushList();
      if (line.trim()) blocks.push(`<p>${formatInline(line.trim())}</p>`);
    }
  });
  flushList();
  return blocks.join('');
}
function icon(name) { return `<i data-lucide="${name}"></i>`; }
function refreshIcons() { if (window.lucide) window.lucide.createIcons(); }
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('visible'), 2600);
}

function navigate(viewName) {
  const view = document.getElementById(`view-${viewName}`);
  if (!view) return;
  if (viewName === 'login') {
    document.getElementById('login-form').reset();
    document.getElementById('login-form').hidden = true;
    document.getElementById('login-gate').hidden = false;
    document.getElementById('login-status').textContent = '';
  }
  document.querySelectorAll('.view').forEach(item => item.classList.toggle('active', item === view));
  document.querySelectorAll('.nav-link[data-view]').forEach(item => item.classList.toggle('active', item.dataset.view === viewName));
  document.getElementById('stay-aware-link').classList.toggle('active', viewName === 'stay-aware');
  document.body.classList.toggle('hub-active', viewName === 'stay-aware');
  document.getElementById('page-crumb').textContent = view.dataset.title;
  document.title = `${view.dataset.title} | CyberGuard AI`;
  if (viewName === 'stay-aware') renderHubJourney();
  closeSidebar();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.querySelector('.sidebar-scrim').classList.remove('visible');
}
function openSidebar() {
  document.getElementById('sidebar').classList.add('open');
  document.querySelector('.sidebar-scrim').classList.add('visible');
}

function messageMarkup(role, message, time, pending = false) {
  const isAssistant = role === 'assistant';
  const body = pending
    ? '<div class="typing-indicator" aria-label="CyberGuard is typing"><i></i><i></i><i></i></div>'
    : isAssistant ? formatAssistantContent(message) : `<p>${escapeHtml(message)}</p>`;
  return `<article class="message ${isAssistant ? 'assistant-message' : 'user-message'} ${pending ? 'pending-message' : ''}"><span class="message-avatar">${isAssistant ? icon('bot') : 'JD'}</span><div class="message-body"><div class="message-meta"><strong>${isAssistant ? 'CyberGuard AI' : 'You'}</strong><time>${time}</time></div><div class="message-content">${body}</div></div></article>`;
}
function formatTime(date = new Date()) { return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }); }
function readChat() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE.chat) || '[]');
    return Array.isArray(saved) ? saved : [];
  } catch { return []; }
}
function saveChat(messages) { localStorage.setItem(STORAGE.chat, JSON.stringify(messages.slice(-40))); }
function renderChat() {
  const container = document.getElementById('chat-messages');
  if (!container) return;
  const messages = readChat();
  if (!messages.length) {
    container.innerHTML = `<div class="chat-welcome"><span class="welcome-chat-icon">${icon('shield-check')}</span><span class="eyebrow">A SAFER INTERNET STARTS HERE</span><h2>What’s on your mind?</h2><p>Ask a question, or choose a quick prompt below.</p></div>`;
  } else {
    container.innerHTML = messages.map(item => messageMarkup(item.role, item.text, item.time)).join('');
  }
  container.scrollTop = container.scrollHeight;
  refreshIcons();
}
async function sendChatMessage(rawMessage) {
  const message = rawMessage.trim();
  if (!message) return;
  const messages = readChat();
  const userMessage = { role: 'user', text: message, time: formatTime() };
  messages.push(userMessage);
  saveChat(messages);
  renderChat();
  navigate('chat');
  const container = document.getElementById('chat-messages');
  const pending = document.createElement('div');
  pending.innerHTML = messageMarkup('assistant', '', formatTime(), true);
  container.append(pending.firstElementChild);
  container.scrollTop = container.scrollHeight;
  refreshIcons();
  await new Promise(resolve => setTimeout(resolve, 750));
  const response = await chatApi.sendMessage(message);
  if (response === null) return;
  const latest = readChat();
  latest.push({ role: 'assistant', text: response, time: formatTime() });
  saveChat(latest);
  renderChat();
}

function renderLearningCards() {
  const container = document.getElementById('learning-grid');
  container.innerHTML = learningGuides.map((guide, index) => `<article class="learning-card"><div class="learning-card-top"><span class="learning-icon">${icon(guide.icon)}</span><span class="learning-tag">${guide.tag}</span></div><h2>${guide.title}</h2><p>${guide.short}</p><button class="text-link" type="button" data-guide="${index}">Read more ${icon('arrow-right')}</button></article>`).join('');
  refreshIcons();
}
function openGuide(index) {
  const guide = learningGuides[index];
  if (!guide) return;
  document.getElementById('dialog-category').textContent = guide.tag;
  document.getElementById('dialog-title').textContent = guide.title;
  document.getElementById('dialog-body').innerHTML = guide.body.map(paragraph => `<p>${escapeHtml(paragraph)}</p>`).join('');
  document.getElementById('dialog-tip').textContent = guide.tip;
  document.getElementById('dialog-icon').innerHTML = icon(guide.icon);
  document.getElementById('dialog-references').innerHTML = guide.references.map(([label, url]) => `<li><a href="${url}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)} ${icon('arrow-up-right')}</a></li>`).join('');
  document.getElementById('guide-dialog').showModal();
  refreshIcons();
}

function readAssessmentScores() {
  try {
    const scores = JSON.parse(localStorage.getItem('cyberguard.quizScores') || '{}');
    return scores && typeof scores === 'object' ? scores : {};
  } catch {
    return {};
  }
}
function assessmentQuestions(index) {
  return Array.from({ length: questionsPerAssessment }, (_, offset) => quizQuestions[(index * 3 + offset * 7) % quizQuestions.length]);
}
function renderAssessmentPicker() {
  const grid = document.getElementById('assessment-grid');
  const scores = readAssessmentScores();
  grid.innerHTML = Array.from({ length: assessmentCount }, (_, index) => {
    const label = `Assessment ${String(index + 1).padStart(2, '0')}`;
    const best = scores[index] === undefined ? 'Not taken' : `Best ${scores[index]}/5`;
    return `<button class="assessment-card" type="button" data-assessment="${index}"><span class="assessment-number">${String(index + 1).padStart(2, '0')}</span><strong>${label}</strong><small>5 questions · ${best}</small><span class="assessment-arrow">${icon('arrow-up-right')}</span></button>`;
  }).join('');
  refreshIcons();
}
function renderQuizBest() {
  const values = Object.values(readAssessmentScores()).map(Number).filter(Number.isFinite);
  const storedLegacyScore = savedQuizScore();
  if (storedLegacyScore !== null && Number.isFinite(Number(storedLegacyScore))) values.push(Number(storedLegacyScore));
  const best = values.length ? Math.max(...values) : null;
  document.querySelector('#quiz-best strong').textContent = best === null ? '--' : `${best}/5`;
}
function renderQuizQuestion() {
  const shell = document.getElementById('quiz-shell');
  const question = activeQuestions[quizIndex];
  const answered = selectedAnswer !== null;
  shell.innerHTML = `<div class="quiz-topline"><span>Assessment ${String(activeAssessment + 1).padStart(2, '0')} · Question ${quizIndex + 1} of ${questionsPerAssessment}</span><button class="text-button" type="button" data-assessment-back>${icon('arrow-left')} All assessments</button></div><div class="progress-track" aria-label="Quiz progress"><span style="width:${((quizIndex + 1) / questionsPerAssessment) * 100}%"></span></div><span class="quiz-topic">${icon('sparkles')} ${question.topic}</span><h2 class="quiz-question">${question.question}</h2><div class="quiz-options" role="group" aria-label="Answer options">${question.options.map((option, index) => `<button class="quiz-option ${answered && index === question.answer ? 'correct' : ''} ${answered && index === selectedAnswer && index !== question.answer ? 'incorrect' : ''}" type="button" data-answer="${index}" ${answered ? 'disabled' : ''}><span class="option-letter">${String.fromCharCode(65 + index)}</span><span>${option}</span>${answered && index === question.answer ? icon('check') : ''}</button>`).join('')}</div>${answered ? `<div class="quiz-feedback">${icon(selectedAnswer === question.answer ? 'circle-check' : 'lightbulb')}<span>${selectedAnswer === question.answer ? 'That’s right. ' : 'Not quite. '}${question.explanation}</span></div>` : ''}<div class="quiz-next-row">${answered ? `<button class="primary-button" id="quiz-next" type="button">${quizIndex === questionsPerAssessment - 1 ? 'See my results' : 'Next question'} ${icon('arrow-right')}</button>` : '<button class="primary-button" type="button" disabled>Choose an answer</button>'}</div>`;
  refreshIcons();
}
let quizIndex = 0;
let quizScore = 0;
let selectedAnswer = null;
let activeAssessment = 0;
let activeQuestions = [];
function startQuiz(index) {
  activeAssessment = index;
  activeQuestions = assessmentQuestions(index);
  quizIndex = 0;
  quizScore = 0;
  selectedAnswer = null;
  document.getElementById('assessment-grid').hidden = true;
  document.getElementById('quiz-shell').hidden = false;
  renderQuizQuestion();
}
function chooseAnswer(index) {
  if (selectedAnswer !== null) return;
  selectedAnswer = index;
  if (index === quizQuestions[quizIndex].answer) quizScore += 1;
  renderQuizQuestion();
}
function finishQuiz() {
  localStorage.setItem(STORAGE.quizScore, String(quizScore));
  const scores = readAssessmentScores();
  scores[activeAssessment] = Math.max(Number(scores[activeAssessment] ?? 0), quizScore);
  localStorage.setItem('cyberguard.quizScores', JSON.stringify(scores));
  safetyScore = Math.round((82 * 0.65) + ((quizScore / questionsPerAssessment) * 100 * 0.35));
  localStorage.setItem(STORAGE.safetyScore, String(safetyScore));
  renderQuizBest();
  renderAssessmentPicker();
  renderScore();
  const shell = document.getElementById('quiz-shell');
  const percentage = Math.round((quizScore / questionsPerAssessment) * 100);
  const message = percentage >= 80 ? 'You’ve got strong instincts.' : percentage >= 60 ? 'You’re building good habits.' : 'Every question is a chance to get safer.';
  shell.innerHTML = `<div class="quiz-result"><span class="result-medal">${icon('trophy')}</span><span class="eyebrow">ASSESSMENT ${String(activeAssessment + 1).padStart(2, '0')} COMPLETE</span><h2>${message}</h2><p>Your best score is saved on this device. Keep practicing the habits that protect your accounts.</p><div class="result-score"><strong>${quizScore}</strong><span>/ ${questionsPerAssessment} correct</span></div><div><button class="primary-button" type="button" data-go="score">View safety score ${icon('arrow-right')}</button> <button class="secondary-button" id="restart-quiz" type="button">Try again</button></div></div>`;
  refreshIcons();
}

const scoreCategories = [
  { name: 'Password Security', score: 90 },
  { name: 'Phishing Awareness', score: 75 },
  { name: 'MFA Usage', score: 80 },
  { name: 'Scam Awareness', score: 70 },
  { name: 'General Knowledge', score: 85 }
];
function renderScore() {
  safetyScore = readNumber(STORAGE.safetyScore, safetyScore);
  document.getElementById('score-value').textContent = safetyScore;
  document.getElementById('score-ring').style.background = `conic-gradient(var(--green) 0 ${safetyScore}%, rgba(114,130,154,.15) ${safetyScore}% 100%)`;
  const grade = safetyScore >= 85 ? 'EXCELLENT' : safetyScore >= 70 ? 'GOOD' : safetyScore >= 50 ? 'FAIR' : 'NEEDS WORK';
  document.getElementById('score-grade').textContent = grade;
  document.getElementById('score-callout-copy').textContent = safetyScore >= 85
    ? 'Keep your strong habits going: review account recovery options and security alerts.'
    : safetyScore >= 70
      ? 'Turn on multi-factor authentication for your email and financial accounts.'
      : 'Start with unique passwords and multi-factor authentication on your most important accounts.';
  document.getElementById('score-breakdown').innerHTML = scoreCategories.map(item => `<div class="breakdown-item"><div class="breakdown-item-head"><strong>${item.name}</strong><b style="color:${item.score >= 80 ? 'var(--green)' : item.score >= 70 ? 'var(--amber)' : 'var(--red)'}">${item.score}<small style="font-size:8px;color:#748097">/100</small></b></div><div class="breakdown-track"><span style="width:${item.score}%"></span></div></div>`).join('');
}

const HOME_SECURITY_TIPS = [
  { text: 'Never share an OTP, even if someone claims to be from your bank.' },
  { text: 'Use a different strong password for every important account.' },
  { text: 'Check the sender before opening unexpected links.' },
  { text: 'Avoid sensitive transactions on public Wi-Fi.' },
  { text: 'Keep your phone and apps updated.' }
];
const HUB_THREATS = {
  delivery: { title: 'Fake delivery SMS', level: 'High', text: 'Unexpected delivery texts may use a fake fee or address problem to lead to a credential-stealing website. Check shipment status through the carrier’s official app or site.' },
  job: { title: 'Job / internship scams', level: 'High', text: 'Be cautious of offers made without a real interview, requests for upfront payment, or checks that ask you to return part of the money. Verify the employer using its official careers page.' },
  qr: { title: 'QR code scams', level: 'Medium', text: 'A QR code can hide a link to a fake sign-in or payment page. Preview the destination and go to the service’s official app or website directly.' },
  phishing: { title: 'Phishing emails', level: 'Medium', text: 'Unexpected urgency, mismatched domains, attachments, and requests for passwords or payment details deserve extra scrutiny. Verify through a known official channel.' },
  malware: { title: 'Malware in attachments', level: 'Low', text: 'Unexpected files can contain harmful software. Confirm with the sender using a separate channel and keep your device protection up to date.' }
};
const HUB_CHECKLISTS = {
  privacy: [
    ['profile-visibility', 'Review profile visibility', 'Limit personal details to the audience you intend.'],
    ['location-sharing', 'Review location sharing', 'Turn off continuous location access where it is not needed.'],
    ['app-permissions', 'Check app permissions', 'Remove access to contacts, microphone, or camera when unnecessary.'],
    ['data-sharing', 'Review data-sharing choices', 'Check privacy controls for social, shopping, and mobile apps.']
  ],
  device: [
    ['system-updates', 'Install system updates', 'Use your device settings to check for updates.'],
    ['screen-lock', 'Use a secure screen lock', 'Choose a strong PIN or biometric lock.'],
    ['device-finding', 'Enable device finding', 'Check the official lost-device feature for your platform.'],
    ['device-backup', 'Check your backup', 'Make sure important data has a recent, recoverable backup.']
  ],
  wifi: [
    ['router-password', 'Change the router admin password', 'Do not keep the manufacturer default.'],
    ['wifi-encryption', 'Use WPA2 or WPA3 security', 'Choose the strongest option supported by your router.'],
    ['router-updates', 'Check router updates', 'Use the manufacturer’s official settings and support.'],
    ['guest-network', 'Use a guest network', 'Keep visitors and smart devices separate when possible.']
  ],
  cleanup: [
    ['old-accounts', 'Old accounts', 'Close accounts you no longer use.'],
    ['unused-apps', 'Unused apps', 'Remove apps that are no longer needed.'],
    ['browser-permissions', 'Old browser permissions', 'Remove access granted to sites you no longer trust.'],
    ['saved-passwords', 'Saved passwords', 'Review and update reused or outdated passwords.'],
    ['unknown-subscriptions', 'Unknown subscriptions', 'Review recurring payments and cancel unfamiliar ones.']
  ]
};
const HUB_EMERGENCIES = {
  hacked: { title: 'My account was hacked', steps: ['Use the service’s official recovery page from a trusted device.', 'Change the password and any reused passwords.', 'Sign out other sessions, review recovery details, and enable multi-factor authentication.', 'Tell your contacts if messages may have been sent from your account.'] },
  stolen: { title: 'My phone was stolen', steps: ['Use the manufacturer’s official lost-device service to lock or locate it.', 'Contact your mobile carrier and workplace or school IT support if applicable.', 'Change important account passwords from another trusted device.', 'Contact your bank if payment cards or banking access may be exposed.'] },
  payment: { title: 'My card or payment was compromised', steps: ['Contact your bank or payment provider using the number on your card or official app.', 'Freeze or replace the card and dispute unauthorized transactions.', 'Change credentials for affected payment accounts.', 'Save transaction records and report suspected fraud to the relevant authority.'] },
  download: { title: 'I downloaded something suspicious', steps: ['Do not open the file or enter passwords on the device.', 'Use trusted security software to scan the device.', 'If you entered credentials, change them using a separate trusted device.', 'Contact trusted IT support if this is a work or school device.'] },
  impersonation: { title: 'Someone is impersonating me', steps: ['Secure the affected account through the platform’s official help center.', 'Report the fake profile or messages and save relevant evidence.', 'Warn people who may receive messages from the impersonator.', 'Change reused passwords and review active sessions.'] }
};
const HUB_STORAGE_PREFIX = 'cyberguard.hub.';
let homeTipIndex = 0;
let hubSelectedDate = null;

function readHubState(key, fallback = {}) {
  try {
    const value = JSON.parse(localStorage.getItem(`${HUB_STORAGE_PREFIX}${key}`) || 'null');
    return value && typeof value === 'object' ? value : fallback;
  } catch {
    return fallback;
  }
}
function writeHubState(key, value) {
  localStorage.setItem(`${HUB_STORAGE_PREFIX}${key}`, JSON.stringify(value));
}
function openHubDialog(title, content) {
  document.getElementById('hub-dialog-title').textContent = title;
  document.getElementById('hub-dialog-content').innerHTML = content;
  const dialog = document.getElementById('hub-dialog');
  if (!dialog.open) dialog.showModal();
  refreshIcons();
}
function renderHubChecklist(group, title, description, initial = {}) {
  const items = HUB_CHECKLISTS[group];
  const state = readHubState(`checklist-${group}`, initial);
  const rows = items.map(([id, label, detail]) => `<label class="hub-check-row"><input type="checkbox" data-hub-check="${group}" data-hub-item="${id}" ${state[id] ? 'checked' : ''}><span><strong>${label}</strong><small>${detail}</small></span></label>`).join('');
  openHubDialog(title, `<p class="hub-dialog-intro">${description}</p><div class="hub-checklist">${rows}</div><p class="hub-dialog-note">Your checklist is saved in this browser only.</p>`);
}
function renderHubThreats() {
  const rows = Object.entries(HUB_THREATS).map(([id, threat]) => `<button class="hub-threat-detail-row" type="button" data-threat="${id}"><span class="threat-dot threat-${threat.level.toLowerCase()}"></span><span><strong>${escapeHtml(threat.title)}</strong><small>${escapeHtml(threat.text)}</small></span><b class="severity-${threat.level.toLowerCase()}">${threat.level}</b></button>`).join('');
  openHubDialog('Current Threats', `<p class="hub-dialog-intro">Awareness feed only. Use the Phishing Detector to inspect a specific message.</p><div class="hub-threat-detail-list">${rows}</div>`);
}
function renderHubThreat(id) {
  const threat = HUB_THREATS[id];
  if (!threat) return;
  openHubDialog(threat.title, `<span class="hub-risk-label severity-${threat.level.toLowerCase()}">${threat.level} awareness</span><p class="hub-dialog-intro">${escapeHtml(threat.text)}</p><div class="hub-safe-callout"><i data-lucide="shield-check"></i><span>Verify through the service’s official app or a contact method you already trust.</span></div>`);
}
function renderHubEmergency() {
  const scenarios = Object.entries(HUB_EMERGENCIES).map(([id, scenario]) => `<button class="hub-scenario-button" type="button" data-emergency="${id}"><span>${escapeHtml(scenario.title)}</span><i data-lucide="arrow-right"></i></button>`).join('');
  openHubDialog('Emergency Cyber Guide', `<p class="hub-dialog-intro">Choose what happened for immediate, defensive next steps. If you are in immediate danger or money is at risk, contact the relevant local authorities or financial provider.</p><div class="hub-scenario-list">${scenarios}</div>`);
}
function renderEmergencySteps(id) {
  const scenario = HUB_EMERGENCIES[id];
  if (!scenario) return;
  const steps = scenario.steps.map(step => `<li>${escapeHtml(step)}</li>`).join('');
  openHubDialog(scenario.title, `<ol class="hub-emergency-steps">${steps}</ol><button class="text-link" type="button" data-hub-tool="emergency"><i data-lucide="arrow-left"></i> All emergency scenarios</button>`);
}
function renderHubAccounts() {
  const services = ['Google', 'Instagram', 'Email', 'Banking', 'College'];
  const statuses = ['Strong', 'Review', 'Needs Attention'];
  const state = readHubState('accounts', { Google: 'Strong', Instagram: 'Review', Email: 'Strong', Banking: 'Review', College: 'Needs Attention' });
  const rows = services.map(service => `<label class="hub-account-row"><span><i data-lucide="circle-user-round"></i><strong>${service}</strong></span><select data-hub-account="${service}" aria-label="${service} security status">${statuses.map(status => `<option ${state[service] === status ? 'selected' : ''}>${status}</option>`).join('')}</select></label>`).join('');
  openHubDialog('Account Protection Center', `<p class="hub-dialog-intro">Track your own review status. This does not connect to or inspect your accounts.</p><div class="hub-account-list">${rows}</div><p class="hub-dialog-note">Use unique passwords and multi-factor authentication wherever available.</p>`);
}
function renderHubCalendar() {
  if (!hubSelectedDate) {
    const today = new Date();
    const dayOffset = (today.getDay() + 6) % 7;
    const monday = new Date(today);
    monday.setDate(today.getDate() - dayOffset);
    hubSelectedDate = monday.toISOString().slice(0, 10);
  }
  const monday = new Date(`${hubSelectedDate}T12:00:00`);
  monday.setDate(monday.getDate() - ((monday.getDay() + 6) % 7));
  const days = Array.from({ length: 7 }, (_, index) => {
    const date = new Date(monday);
    date.setDate(monday.getDate() + index);
    const key = date.toISOString().slice(0, 10);
    return `<button class="hub-calendar-day ${key === hubSelectedDate ? 'selected' : ''}" type="button" data-calendar-date="${key}" aria-pressed="${key === hubSelectedDate}"><small>${date.toLocaleDateString(undefined, { weekday: 'short' })}</small><strong>${date.getDate()}</strong></button>`;
  }).join('');
  const tasks = ['Review one account’s sign-in activity', 'Check for device or app updates', 'Back up an important file'];
  const state = readHubState(`calendar-${hubSelectedDate}`, {});
  const checklist = tasks.map((task, index) => `<label class="hub-calendar-task"><input type="checkbox" data-hub-calendar-task="${index}" ${state[index] ? 'checked' : ''}><span>${task}</span></label>`).join('');
  openHubDialog('Security Calendar', `<p class="hub-dialog-intro">Pick a day and mark a small security habit complete.</p><div class="hub-calendar-grid">${days}</div><p class="hub-calendar-selected">${new Date(`${hubSelectedDate}T12:00:00`).toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' })}</p><div class="hub-calendar-tasks">${checklist}</div>`);
}
function renderHubReport() {
  const values = [...document.querySelectorAll('[data-journey]')].map(node => `<div class="hub-report-row"><span>${node.parentElement.querySelector('strong').textContent}</span><strong>${node.textContent}</strong></div>`).join('');
  openHubDialog('Security Journey Report', `<p class="hub-dialog-intro">Your current journey estimates help you choose a useful next step. Checklist progress stays on this device.</p><div class="hub-report-list">${values}</div><button class="primary-button" type="button" data-go="score">Open Safety Score <i data-lucide="arrow-right"></i></button>`);
}
function openHubTool(name) {
  const actions = {
    threats: renderHubThreats,
    privacy: () => renderHubChecklist('privacy', 'Privacy Checkup', 'Review these settings on the apps and services you use.'),
    device: () => renderHubChecklist('device', 'Device Safety Center', 'A guided self-check only; this page does not scan your device.'),
    wifi: () => renderHubChecklist('wifi', 'Wi-Fi Safety Check', 'This is a manual safety checklist. It does not scan your network.'),
    emergency: renderHubEmergency,
    accounts: renderHubAccounts,
    cleanup: () => renderHubChecklist('cleanup', 'Digital Cleanup', 'Check off items as you review them.', { 'old-accounts': true, 'unused-apps': true }),
    calendar: renderHubCalendar,
    report: renderHubReport,
    actions: () => renderHubChecklist('cleanup', 'Your Security Actions', 'Three cleanup items are ready for review.', { 'old-accounts': true, 'unused-apps': true })
  };
  actions[name]?.();
}
function renderHomeSecurityTip() {
  const tip = HOME_SECURITY_TIPS[homeTipIndex];
  document.getElementById('home-tip-text').textContent = tip.text;
  document.getElementById('home-tip-dots').innerHTML = HOME_SECURITY_TIPS.map((_, index) => `<button type="button" data-home-tip-index="${index}" aria-label="Show security tip ${index + 1}" aria-current="${index === homeTipIndex}"></button>`).join('');
}
function initializeHomeSecurityTips() {
  renderHomeSecurityTip();
  document.getElementById('home-tip-prev').addEventListener('click', () => {
    homeTipIndex = (homeTipIndex + HOME_SECURITY_TIPS.length - 1) % HOME_SECURITY_TIPS.length;
    renderHomeSecurityTip();
  });
  document.getElementById('home-tip-next').addEventListener('click', () => {
    homeTipIndex = (homeTipIndex + 1) % HOME_SECURITY_TIPS.length;
    renderHomeSecurityTip();
  });
  document.getElementById('home-tip-dots').addEventListener('click', event => {
    const dot = event.target.closest('[data-home-tip-index]');
    if (dot) { homeTipIndex = Number(dot.dataset.homeTipIndex); renderHomeSecurityTip(); }
  });
  window.setInterval(() => {
    homeTipIndex = (homeTipIndex + 1) % HOME_SECURITY_TIPS.length;
    renderHomeSecurityTip();
  }, 7000);
}
function renderHubJourney() {
  const scoreData = localStorage.getItem(STORAGE.safetyScore);
  const assessmentData = readAssessmentScores();
  const assessmentScores = Object.values(assessmentData).map(Number).filter(Number.isFinite);
  const quizScore = assessmentScores.length ? Math.round(Math.max(...assessmentScores) * 20) : 60;
  const accountData = localStorage.getItem(`${HUB_STORAGE_PREFIX}accounts`);
  const privacyData = localStorage.getItem(`${HUB_STORAGE_PREFIX}checklist-privacy`);
  const deviceData = localStorage.getItem(`${HUB_STORAGE_PREFIX}checklist-device`);
  const percentChecked = key => {
    const state = readHubState(key, {});
    const checklist = HUB_CHECKLISTS[key.replace('checklist-', '')] || [];
    return checklist.length ? Math.round(checklist.filter(([id]) => state[id]).length / checklist.length * 100) : 0;
  };
  const accountPercent = accountData ? Math.round(Object.values(readHubState('accounts')).filter(status => status === 'Strong').length / 5 * 100) : 75;
  const values = {
    accounts: accountPercent,
    privacy: privacyData ? percentChecked('checklist-privacy') : 50,
    device: deviceData ? percentChecked('checklist-device') : 80,
    quiz: quizScore,
    overall: scoreData === null ? 85 : Math.min(100, Math.max(0, Number(scoreData)))
  };
  Object.entries(values).forEach(([key, value]) => {
    const node = document.querySelector(`[data-journey="${key}"]`);
    if (!node) return;
    node.textContent = `${value}%`;
    node.parentElement.querySelector('.journey-progress i').style.setProperty('--journey-progress', `${value}%`);
  });
  const cleanup = readHubState('checklist-cleanup', { 'old-accounts': true, 'unused-apps': true });
  const pending = HUB_CHECKLISTS.cleanup.filter(([id]) => !cleanup[id]).length;
  document.getElementById('hub-pending-actions').textContent = `${pending} security action${pending === 1 ? '' : 's'}`;
}
function initializeStayAwareHub() {
  document.querySelectorAll('[data-hub-tool]').forEach(button => button.addEventListener('click', () => openHubTool(button.dataset.hubTool)));
  document.querySelectorAll('[data-threat]').forEach(button => button.addEventListener('click', () => renderHubThreat(button.dataset.threat)));
  document.getElementById('hub-dialog').addEventListener('click', event => {
    if (event.target.closest('.hub-dialog-close')) document.getElementById('hub-dialog').close();
    const tool = event.target.closest('[data-hub-tool]');
    if (tool) openHubTool(tool.dataset.hubTool);
    const threat = event.target.closest('[data-threat]');
    if (threat) renderHubThreat(threat.dataset.threat);
    const scenario = event.target.closest('[data-emergency]');
    if (scenario) renderEmergencySteps(scenario.dataset.emergency);
    const date = event.target.closest('[data-calendar-date]');
    if (date) { hubSelectedDate = date.dataset.calendarDate; renderHubCalendar(); }
    const route = event.target.closest('[data-go]');
    if (route) { document.getElementById('hub-dialog').close(); navigate(route.dataset.go); }
  });
  document.getElementById('hub-dialog').addEventListener('change', event => {
    const checkbox = event.target.closest('[data-hub-check]');
    if (checkbox) {
      const state = readHubState(`checklist-${checkbox.dataset.hubCheck}`, {});
      state[checkbox.dataset.hubItem] = checkbox.checked;
      writeHubState(`checklist-${checkbox.dataset.hubCheck}`, state);
      renderHubJourney();
    }
    const account = event.target.closest('[data-hub-account]');
    if (account) {
      const state = readHubState('accounts', { Google: 'Strong', Instagram: 'Review', Email: 'Strong', Banking: 'Review', College: 'Needs Attention' });
      state[account.dataset.hubAccount] = account.value;
      writeHubState('accounts', state);
      renderHubJourney();
    }
    const calendarTask = event.target.closest('[data-hub-calendar-task]');
    if (calendarTask) {
      const key = `calendar-${hubSelectedDate}`;
      const state = readHubState(key, {});
      state[calendarTask.dataset.hubCalendarTask] = calendarTask.checked;
      writeHubState(key, state);
    }
  });
  renderHubJourney();
}

function analyzeMessage() {
  const input = document.getElementById('phishing-input');
  const text = input.value.trim();
  if (!text) {
    input.focus();
    showToast('Paste a message or URL to analyze first.');
    return;
  }
  const lower = text.toLowerCase();
  const signs = [
    { label: 'Urgent or threatening language', detected: /urgent|immediately|account.{0,25}(blocked|suspend|locked|close)|within\s+\d+\s*(hour|minute)|final warning|act now|limited time|verify now|expire/.test(lower) },
    { label: 'Suspicious or shortened link', detected: /https?:\/\/|www\.|bit\.ly|tinyurl|t\.co|\.zip\b|\.top\b|\.xyz\b/.test(lower) },
    { label: 'Unknown or mismatched sender', detected: /dear (customer|user|member)|unknown sender|no-reply@|support@[^\s]*(?!bank|company)|sender:|from:/.test(lower) },
    { label: 'Possible fake or lookalike domain', detected: /paypa[l1]|amaz[o0]n|micros[o0]ft|app[1l]e|bank-secure|secure-login|verify-account|account-update|\.ru\b|\.tk\b/.test(lower) },
    { label: 'Request for personal or payment information', detected: /password|passcode|verification code|social security|credit card|bank details|personal information|account number|confirm.{0,20}(identity|details|payment)/.test(lower) }
  ];
  let risk = signs.filter(item => item.detected).length;
  if (activeContentType === 'Website URL' && !/^https?:\/\//i.test(text)) risk += 1;
  const level = risk >= 3 ? 'high' : risk >= 1 ? 'medium' : 'low';
  const title = level === 'high' ? 'HIGH RISK' : level === 'medium' ? 'CAUTION ADVISED' : 'LOW RISK SIGNALS';
  const subtitle = level === 'high' ? 'This message looks suspicious.' : level === 'medium' ? 'Some details deserve a closer look.' : 'No common warning patterns were detected.';
  const warnings = signs.map(item => `<div class="warning-item ${item.detected ? '' : 'clean'}">${icon(item.detected ? 'circle-alert' : 'circle-check')}<span>${item.label}${item.detected ? '' : ' · not detected'}</span></div>`).join('');
  document.getElementById('analysis-panel').innerHTML = `<div class="risk-result"><div class="risk-banner ${level}"><span class="risk-symbol">${icon(level === 'low' ? 'shield-check' : 'triangle-alert')}</span><span><strong>${title}</strong><small>${subtitle}</small></span><span class="risk-number">${risk}<small style="font-size:9px;color:#8490a5"> / 5</small></span></div><h3>Detected warning signs</h3><div class="warning-list">${warnings}</div><div class="advice-box"><h3>${icon('shield-alert')} What you should do</h3><div class="advice-list"><span>${icon('circle-check')} Do not click the link</span><span>${icon('circle-check')} Do not share personal information</span><span>${icon('circle-check')} Verify through the official website</span><span>${icon('circle-check')} Report the message</span></div></div></div>`;
  refreshIcons();
}

function initSettings() {
  const notifications = document.getElementById('setting-notifications');
  const motion = document.getElementById('setting-motion');
  notifications.checked = localStorage.getItem(STORAGE.notifications) === 'true';
  motion.checked = localStorage.getItem(STORAGE.reduceMotion) === 'true';
  applyTheme(localStorage.getItem(STORAGE.theme) || 'dark');
  document.body.classList.toggle('reduce-motion', motion.checked);
  notifications.addEventListener('change', () => {
    localStorage.setItem(STORAGE.notifications, String(notifications.checked));
    showToast(notifications.checked ? 'Habit reminders are enabled.' : 'Habit reminders are turned off.');
  });
  motion.addEventListener('change', () => {
    localStorage.setItem(STORAGE.reduceMotion, String(motion.checked));
    document.body.classList.toggle('reduce-motion', motion.checked);
  });
  document.querySelectorAll('[data-theme-choice]').forEach(button => {
    button.addEventListener('click', () => applyTheme(button.dataset.themeChoice));
  });
}

function applyTheme(theme) {
  const isLight = theme === 'light';
  document.body.classList.toggle('theme-light', isLight);
  localStorage.setItem(STORAGE.theme, isLight ? 'light' : 'dark');
  document.querySelectorAll('[data-theme-choice]').forEach(button => {
    button.setAttribute('aria-pressed', String(button.dataset.themeChoice === (isLight ? 'light' : 'dark')));
  });
}

function initNotifications() {
  const toggle = document.getElementById('notification-toggle');
  const panel = document.getElementById('notification-panel');
  const unreadItems = panel.querySelectorAll('.notification-list li');
  const unreadCount = localStorage.getItem(STORAGE.notificationsRead) === 'true' ? 0 : unreadItems.length;
  const count = document.getElementById('notification-count');
  const summary = document.getElementById('notification-summary');

  const updateReadState = read => {
    unreadItems.forEach(item => item.classList.toggle('unread', !read));
    count.hidden = read;
    summary.textContent = read ? 'You’re all caught up' : `${unreadItems.length} unread updates`;
    toggle.setAttribute('aria-label', read ? 'Notifications, all read' : `Notifications, ${unreadItems.length} unread`);
  };

  updateReadState(unreadCount === 0);
  toggle.addEventListener('click', () => {
    const isOpen = !panel.hidden;
    panel.hidden = isOpen;
    toggle.setAttribute('aria-expanded', String(!isOpen));
  });
  document.getElementById('mark-notifications-read').addEventListener('click', () => {
    localStorage.setItem(STORAGE.notificationsRead, 'true');
    updateReadState(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.notification-wrap')) {
      panel.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

function initialize() {
  document.querySelectorAll('.nav-link[data-view]').forEach(button => button.addEventListener('click', () => navigate(button.dataset.view)));
  document.querySelectorAll('[data-go]').forEach(button => button.addEventListener('click', () => navigate(button.dataset.go)));
  document.querySelectorAll('[data-view-link]').forEach(link => link.addEventListener('click', event => { event.preventDefault(); navigate(link.dataset.viewLink); }));
  document.getElementById('menu-toggle').addEventListener('click', openSidebar);
  document.querySelector('[data-close-sidebar]').addEventListener('click', closeSidebar);
  document.querySelectorAll('[data-chat-form]').forEach(form => form.addEventListener('submit', event => {
    event.preventDefault();
    const input = form.elements.message;
    const value = input.value;
    input.value = '';
    sendChatMessage(value);
  }));
  document.getElementById('show-login-form').addEventListener('click', () => {
    document.getElementById('login-gate').hidden = true;
    document.getElementById('login-form').hidden = false;
    document.getElementById('login-email').focus();
  });
  document.getElementById('login-form').addEventListener('submit', event => {
    event.preventDefault();
    document.getElementById('login-status').textContent = 'Authentication is not configured yet. Your details were not sent or saved.';
    event.currentTarget.reset();
  });
  const password = document.getElementById('login-password');
  document.getElementById('toggle-password').addEventListener('click', event => {
    const visible = password.type === 'password';
    password.type = visible ? 'text' : 'password';
    event.currentTarget.setAttribute('aria-label', visible ? 'Hide password' : 'Show password');
    event.currentTarget.title = visible ? 'Hide password' : 'Show password';
    event.currentTarget.innerHTML = icon(visible ? 'eye-off' : 'eye');
    refreshIcons();
  });
  document.querySelectorAll('[data-plan]').forEach(button => {
    button.addEventListener('click', () => {
      const plan = button.dataset.plan;
      localStorage.setItem(STORAGE.plan, plan);
      document.querySelectorAll('[data-plan]').forEach(option => {
        option.setAttribute('aria-pressed', String(option === button));
        option.closest('.plan-card').classList.toggle('selected', option === button);
      });
      document.getElementById('plan-status').textContent = plan === 'Starter'
        ? 'Starter free plan selected. Plan access is a preview.'
        : `${plan} subscription preview selected. Checkout is not connected; no payment will be taken.`;
    });
  });
  const planButtons = [...document.querySelectorAll('[data-plan]')];
  const selectedPlan = planButtons.find(button => button.dataset.plan === localStorage.getItem(STORAGE.plan)) || planButtons[0];
  selectedPlan.click();
  document.querySelectorAll('[data-prompt]').forEach(button => button.addEventListener('click', () => sendChatMessage(button.dataset.prompt)));
  document.getElementById('clear-chat').addEventListener('click', () => {
    localStorage.removeItem(STORAGE.chat);
    renderChat();
    showToast('Chat history cleared from this device.');
  });
  document.getElementById('learning-grid').addEventListener('click', event => {
    const button = event.target.closest('[data-guide]');
    if (button) openGuide(Number(button.dataset.guide));
  });
  document.getElementById('dialog-done').addEventListener('click', () => document.getElementById('guide-dialog').close());
  document.querySelector('.dialog-close').addEventListener('click', () => document.getElementById('guide-dialog').close());
  document.getElementById('assessment-grid').addEventListener('click', event => {
    const button = event.target.closest('[data-assessment]');
    if (button) startQuiz(Number(button.dataset.assessment));
  });
  document.getElementById('quiz-shell').addEventListener('click', event => {
    const navigation = event.target.closest('[data-go]');
    if (navigation) {
      navigate(navigation.dataset.go);
      return;
    }
    if (event.target.closest('[data-assessment-back]')) {
      document.getElementById('quiz-shell').hidden = true;
      document.getElementById('assessment-grid').hidden = false;
      renderAssessmentPicker();
      return;
    }
    const answer = event.target.closest('[data-answer]');
    if (answer) chooseAnswer(Number(answer.dataset.answer));
    if (event.target.closest('#quiz-next')) {
      if (quizIndex === questionsPerAssessment - 1) finishQuiz();
      else { quizIndex += 1; selectedAnswer = null; renderQuizQuestion(); }
    }
    if (event.target.closest('#restart-quiz')) startQuiz(activeAssessment);
  });
  document.querySelectorAll('[data-content-type]').forEach(button => button.addEventListener('click', () => {
    activeContentType = button.dataset.contentType;
    document.querySelectorAll('[data-content-type]').forEach(item => item.classList.toggle('active', item === button));
    document.getElementById('content-type-label').textContent = activeContentType.toUpperCase();
    document.getElementById('phishing-input').placeholder = activeContentType === 'Website URL' ? 'Paste the full URL here, including https://...' : `Paste the ${activeContentType.toLowerCase()} here, including any links or sender details...`;
  }));
  document.getElementById('phishing-input').addEventListener('input', event => { document.getElementById('char-count').textContent = `${event.target.value.length} characters`; });
  document.getElementById('analyze-button').addEventListener('click', analyzeMessage);
  document.getElementById('load-sample').addEventListener('click', () => {
    const sample = 'From: Account Security <security@paypaI-account-review.example>\n\nURGENT: Your account will be blocked within 24 hours. Verify your password and payment details immediately: http://bit.ly/account-check';
    const input = document.getElementById('phishing-input');
    input.value = sample;
    document.getElementById('char-count').textContent = `${sample.length} characters`;
    analyzeMessage();
  });
  renderLearningCards();
  renderChat();
  renderAssessmentPicker();
  renderQuizBest();
  renderScore();
  initSettings();
  initNotifications();
  initializeStayAwareHub();
  initializeHomeSecurityTips();
  refreshIcons();
}

document.addEventListener('DOMContentLoaded', initialize);
