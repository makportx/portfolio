// Portfolio Interactive Functionality for Isrel

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // 2. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        // Close on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    // 3. Project Filter Tabs
    const filterButtons = document.querySelectorAll('[data-project-filter]');
    const projectCards = document.querySelectorAll('[data-project-category]');

    if (filterButtons.length > 0 && projectCards.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetCategory = button.getAttribute('data-project-filter');

                // Update active tab style
                filterButtons.forEach(btn => {
                    btn.classList.remove('bg-cyan-500', 'text-slate-950', 'shadow-lg', 'shadow-cyan-500/20');
                    btn.classList.add('bg-slate-800/80', 'text-slate-300');
                });
                button.classList.remove('bg-slate-800/80', 'text-slate-300');
                button.classList.add('bg-cyan-500', 'text-slate-950', 'shadow-lg', 'shadow-cyan-500/20');

                // Filter cards with subtle fade
                projectCards.forEach(card => {
                    const cardCategory = card.getAttribute('data-project-category');
                    if (targetCategory === 'all' || cardCategory === targetCategory) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    // 4. Skills Tab Filter (if used)
    const skillCategoryBtns = document.querySelectorAll('[data-skill-filter]');
    const skillGroups = document.querySelectorAll('[data-skill-group]');

    if (skillCategoryBtns.length > 0 && skillGroups.length > 0) {
        skillCategoryBtns.forEach(button => {
            button.addEventListener('click', () => {
                const filter = button.getAttribute('data-skill-filter');

                skillCategoryBtns.forEach(b => {
                    b.classList.remove('border-cyan-400', 'text-cyan-400', 'bg-cyan-950/40');
                    b.classList.add('border-slate-800', 'text-slate-400');
                });
                button.classList.add('border-cyan-400', 'text-cyan-400', 'bg-cyan-950/40');
                button.classList.remove('border-slate-800', 'text-slate-400');

                skillGroups.forEach(group => {
                    if (filter === 'all' || group.getAttribute('data-skill-group') === filter) {
                        group.style.display = 'block';
                    } else {
                        group.style.display = 'none';
                    }
                });
            });
        });
    }

    // 5. Interactive AI Resume Assistant
    const aiToggleBtn = document.getElementById('ai-assistant-toggle');
    const aiChatBox = document.getElementById('ai-chat-box');
    const aiCloseBtn = document.getElementById('ai-chat-close');
    const aiMessages = document.getElementById('ai-messages');
    const aiInput = document.getElementById('ai-input');
    const aiSendBtn = document.getElementById('ai-send-btn');
    const quickPrompts = document.querySelectorAll('.ai-quick-prompt');

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (aiToggleBtn && aiChatBox) {
        aiToggleBtn.addEventListener('click', () => {
            aiChatBox.classList.toggle('hidden');
            if (!aiChatBox.classList.contains('hidden')) {
                aiInput && aiInput.focus();
            }
        });

        if (aiCloseBtn) {
            aiCloseBtn.addEventListener('click', () => {
                aiChatBox.classList.add('hidden');
            });
        }

        function appendMessage(sender, text) {
            if (!aiMessages) return;
            const messageRow = document.createElement('div');
            messageRow.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-3`;

            const bubble = document.createElement('div');
            bubble.className = `max-w-[85%] text-xs sm:text-sm p-3 rounded-2xl ${
                sender === 'user'
                    ? 'bg-cyan-500 text-slate-950 font-medium rounded-br-none'
                    : 'bg-slate-800 text-slate-200 border border-slate-700/60 rounded-bl-none'
            }`;

            // Convert simple markdown bold and links
            let formattedText = text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="text-cyan-400 underline font-medium">$1</a>')
                .replace(/\n/g, '<br/>');

            bubble.innerHTML = formattedText;
            messageRow.appendChild(bubble);
            aiMessages.appendChild(messageRow);
            aiMessages.scrollTop = aiMessages.scrollHeight;
        }

        function getClientAIResponse(query) {
            const q = (query || '').toLowerCase();
            if (['education', 'college', 'university', 'srm', 'degree', 'study', 'graduat'].some(k => q.includes(k))) {
                return "🎓 **Education Background**:\nIsrel is currently pursuing a **B.Tech in Computer Science (Data Science specialization)** at **SRM Institute of Science and Technology (SRMIST)**, Chennai.\nExpected graduation is **May 2029**.";
            } else if (['skill', 'stack', 'tech', 'language', 'python', 'django', 'react', 'tools'].some(k => q.includes(k))) {
                return "💻 **Technical Skills**:\n• **Web Development**: Django, HTML5, CSS3, JavaScript, React\n• **Programming**: Python, C/C++ (basics)\n• **Data Science**: Data Analysis, Data Visualization (pandas, matplotlib), Computer Vision (OpenCV)\n• **Tools**: Git, GitHub, VS Code, Django Admin & ORM";
            } else if (['project', 'face recognition', 'attendance', 'dashboard', 'assistant', 'work'].some(k => q.includes(k))) {
                return "🚀 **Key Projects**:\n\n1. **Face Recognition Attendance System**: AI-powered biometric attendance tracker using OpenCV (cv2) with a Tkinter GUI.\n2. **Portfolio Website with AI Assistant**: Multi-page portfolio with React, Node.js, and an intelligent assistant.\n3. **Data Dashboards**: Interactive data visualization dashboards built using Python (pandas, matplotlib).\n4. **Django Portfolio Application**: Dynamic web app featuring Django ORM models and resume integration.";
            } else if (['contact', 'email', 'hire', 'reach', 'message', 'phone', 'linkedin', 'location', 'github'].some(k => q.includes(k))) {
                return "📫 **Get in Touch with Isrel**:\n• **Email**: [makportx@gmail.com](mailto:makportx@gmail.com)\n• **LinkedIn**: [linkedin.com/in/isrel](https://linkedin.com/in/isrel)\n• **GitHub**: [github.com/makportx](https://github.com/makportx)\n• **Location**: Chennai, Tamil Nadu, India\n\nYou can also use the contact form on this page to send a direct message!";
            } else if (['strength', 'advantage', 'mindset', 'soft skill'].some(k => q.includes(k))) {
                return "⭐ **Core Strengths**:\n✔ Strong problem-solving mindset\n✔ Quick adaptability to new technologies\n✔ Passion for merging design aesthetics with solid engineering\n✔ Interest in software development and data-driven insights";
            } else if (['goal', 'career', 'objective', 'future'].some(k => q.includes(k))) {
                return "🎯 **Career Objective**:\nTo grow as a Web Developer & Data Scientist, contributing to innovative projects that combine creativity, data, and technology while continuously learning in a dynamic environment.";
            } else if (['hi', 'hello', 'hey', 'who are you'].some(k => q.includes(k))) {
                return "👋 Hi there! I'm Isrel's AI Portfolio Assistant.\nYou can ask me about:\n• Isrel's projects (Face Recognition, Dashboards, Web apps)\n• Education at SRMIST\n• Technical skills in Python, Django, React, and Data Science\n• How to contact Isrel";
            } else {
                return "Thanks for asking! Isrel is an aspiring Web Developer & Data Science enthusiast studying at SRMIST with strong skills in Python, Django, React, and Data Science.\n\nFeel free to ask about his projects, education, technical skills, or send him an email at [makportx@gmail.com](mailto:makportx@gmail.com)!";
            }
        }

        async function sendQuery(queryText) {
            if (!queryText.trim()) return;

            appendMessage('user', queryText);
            if (aiInput) aiInput.value = '';

            // Typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.id = 'ai-typing-indicator';
            typingIndicator.className = 'flex justify-start mb-3 text-xs text-slate-400 italic';
            typingIndicator.innerHTML = '<span class="px-3 py-1.5 rounded-xl bg-slate-800 border border-slate-700">Thinking...</span>';
            aiMessages.appendChild(typingIndicator);
            aiMessages.scrollTop = aiMessages.scrollHeight;

            try {
                const csrftoken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]')?.value);
                const response = await fetch('/api/ai-assistant/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken || '',
                    },
                    body: JSON.stringify({ query: queryText }),
                });

                if (!response.ok) {
                    throw new Error('API unavailable');
                }

                const data = await response.json();
                typingIndicator.remove();

                if (data && data.response) {
                    appendMessage('ai', data.response);
                } else {
                    appendMessage('ai', getClientAIResponse(queryText));
                }
            } catch (err) {
                if (typingIndicator) typingIndicator.remove();
                appendMessage('ai', getClientAIResponse(queryText));
            }
        }

        if (aiSendBtn && aiInput) {
            aiSendBtn.addEventListener('click', () => {
                sendQuery(aiInput.value);
            });

            aiInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    sendQuery(aiInput.value);
                }
            });
        }

        quickPrompts.forEach(chip => {
            chip.addEventListener('click', () => {
                const query = chip.getAttribute('data-prompt') || chip.innerText.trim();
                sendQuery(query);
            });
        });
    }

    // 6. Contact Form Static Fallback Support
    const contactForm = document.querySelector('form[action*="#contact"]');
    if (contactForm && (window.location.hostname.endsWith('github.io') || window.location.protocol === 'file:')) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = (contactForm.querySelector('[name=name]')?.value || '').trim();
            const email = (contactForm.querySelector('[name=email]')?.value || '').trim();
            const subject = (contactForm.querySelector('[name=subject]')?.value || 'Portfolio Contact').trim();
            const message = (contactForm.querySelector('[name=message]')?.value || '').trim();

            const mailtoUrl = `mailto:makportx@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent('From: ' + name + ' (' + email + ')\n\n' + message)}`;
            
            // Insert confirmation banner above button
            let statusBanner = document.getElementById('contact-status-banner');
            if (!statusBanner) {
                statusBanner = document.createElement('div');
                statusBanner.id = 'contact-status-banner';
                statusBanner.className = 'p-4 rounded-xl bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 text-xs sm:text-sm mb-4';
                contactForm.insertBefore(statusBanner, contactForm.querySelector('button[type=submit]'));
            }
            statusBanner.innerHTML = `✓ Opening your email client to send your message to <strong>makportx@gmail.com</strong>...<br/><a href="${mailtoUrl}" class="underline text-cyan-400 font-semibold mt-1 inline-block">Click here if your mail app didn't open automatically</a>`;
            
            window.location.href = mailtoUrl;
        });
    }
});
