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

                const data = await response.json();
                typingIndicator.remove();

                if (data.response) {
                    appendMessage('ai', data.response);
                } else {
                    appendMessage('ai', "I'm sorry, I couldn't process that. Feel free to contact Isrel directly!");
                }
            } catch (err) {
                if (typingIndicator) typingIndicator.remove();
                appendMessage('ai', "Thanks for reaching out! You can check out Isrel's projects or message him using the form below.");
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
});
