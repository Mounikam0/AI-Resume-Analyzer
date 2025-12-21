const API_URL = 'http://localhost:8000';

let currentAnalysis = null;
let matchResumeText = null;

// Tab Navigation
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.add('hidden'));
    document.querySelectorAll('[id$="Tab"]').forEach(btn => {
        btn.classList.remove('tab-active');
        btn.classList.add('text-gray-500');
    });
    
    // Show selected tab
    document.getElementById(tabName + 'Content').classList.remove('hidden');
    const activeBtn = document.getElementById(tabName + 'Tab');
    activeBtn.classList.add('tab-active');
    activeBtn.classList.remove('text-gray-500');
}

// ========== ANALYZE TAB ==========

document.getElementById('resumeFile').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileInfo').classList.remove('hidden');
    } else {
        alert('Please upload a PDF file');
        e.target.value = '';
    }
});

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('resumeFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file first');
        return;
    }

    document.getElementById('loadingOverlay').classList.remove('hidden');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Analysis failed');

        const data = await response.json();
        currentAnalysis = data.analysis;
        
        displayResults(currentAnalysis);
        document.getElementById('resultsSection').classList.remove('hidden');
        
    } catch (error) {
        console.error('Error:', error);
        alert('Analysis failed. Make sure the backend is running.');
    } finally {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }
});

function displayResults(analysis) {
    const scoreCards = document.getElementById('scoreCards');
    const scores = [
        { label: 'Overall', value: analysis.overallScore },
        { label: 'ATS', value: analysis.atsScore },
        { label: 'Content', value: analysis.contentScore },
        { label: 'Format', value: analysis.formatScore }
    ];

    scoreCards.innerHTML = scores.map(score => {
        const colorClass = score.value >= 80 ? 'border-green-500 bg-green-50 text-green-700' : 
                          score.value >= 60 ? 'border-yellow-500 bg-yellow-50 text-yellow-700' : 
                          'border-red-500 bg-red-50 text-red-700';
        return `
            <div class="bg-white rounded-xl shadow-lg p-6 border-2 ${colorClass}">
                <p class="text-sm font-medium mb-2">${score.label}</p>
                <p class="text-5xl font-bold">${score.value}</p>
                <p class="text-xs mt-1">/ 100</p>
            </div>
        `;
    }).join('');

    const detailedAnalysis = document.getElementById('detailedAnalysis');
    detailedAnalysis.innerHTML = `
        <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-xl font-bold mb-4">
                <i class="fas fa-file-alt text-blue-600 mr-2"></i>Section Analysis
            </h3>
            <div class="space-y-3">
                ${Object.entries(analysis.sections).map(([key, section]) => `
                    <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div class="flex items-center gap-3 flex-1">
                            <i class="fas fa-${section.status === 'good' ? 'check-circle text-green-600' : 
                                               section.status === 'warning' ? 'exclamation-circle text-yellow-600' : 
                                               'times-circle text-red-600'}"></i>
                            <div>
                                <p class="font-semibold capitalize">${key}</p>
                                <p class="text-sm text-gray-600">${section.message}</p>
                            </div>
                        </div>
                        <div class="text-2xl font-bold">${section.score}</div>
                    </div>
                `).join('')}
            </div>
        </div>

        <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-green-600 mb-4">
                    <i class="fas fa-check-circle mr-2"></i>Strengths
                </h3>
                <ul class="space-y-2">
                    ${analysis.strengths.map(s => `
                        <li class="flex gap-2 text-gray-700">
                            <i class="fas fa-check text-green-600 mt-1"></i>
                            <span>${s}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-yellow-600 mb-4">
                    <i class="fas fa-exclamation-triangle mr-2"></i>Improvements
                </h3>
                <ul class="space-y-2">
                    ${analysis.improvements.map(i => `
                        <li class="flex gap-2 text-gray-700">
                            <i class="fas fa-arrow-right text-yellow-600 mt-1"></i>
                            <span>${i}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        </div>

        <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-blue-600 mb-4">Found Skills</h3>
                <div class="flex flex-wrap gap-2">
                    ${analysis.extractedSkills.map(s => `
                        <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">${s}</span>
                    `).join('')}
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-red-600 mb-4">Missing Keywords</h3>
                <div class="flex flex-wrap gap-2">
                    ${analysis.missingKeywords.map(k => `
                        <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm">${k}</span>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

document.getElementById('newAnalysisBtn').addEventListener('click', () => {
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('resumeFile').value = '';
    document.getElementById('fileInfo').classList.add('hidden');
});

// ========== BUILDER TAB ==========

function addExperience() {
    const container = document.getElementById('experienceContainer');
    const newItem = document.createElement('div');
    newItem.className = 'experience-item bg-gray-50 p-4 rounded-lg mb-4';
    newItem.innerHTML = `
        <input type="text" placeholder="Job Title" class="w-full p-2 border rounded mb-2">
        <input type="text" placeholder="Company" class="w-full p-2 border rounded mb-2">
        <div class="grid md:grid-cols-2 gap-2 mb-2">
            <input type="text" placeholder="Start Date" class="p-2 border rounded">
            <input type="text" placeholder="End Date" class="p-2 border rounded">
        </div>
        <textarea placeholder="Achievements" class="w-full p-2 border rounded" rows="3"></textarea>
        <button type="button" onclick="this.parentElement.remove()" class="mt-2 text-red-600">
            <i class="fas fa-trash mr-1"></i>Remove
        </button>
    `;
    container.appendChild(newItem);
}

document.getElementById('resumeForm').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Resume generation feature coming soon! For now, this collects your data.');
});

// ========== MATCHER TAB ==========

document.getElementById('matchResumeFile').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
        document.getElementById('matchFileName').textContent = file.name;
        document.getElementById('matchFileName').classList.remove('hidden');
        
        // Extract text from PDF
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch(`${API_URL}/api/analyze`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            matchResumeText = data.extracted_text;
        } catch (error) {
            console.error('Error extracting text:', error);
        }
    }
});

document.getElementById('matchBtn').addEventListener('click', async () => {
    const jobDescription = document.getElementById('jobDescription').value;
    
    if (!matchResumeText) {
        alert('Please upload your resume first');
        return;
    }
    
    if (!jobDescription.trim()) {
        alert('Please paste the job description');
        return;
    }

    document.getElementById('loadingOverlay').classList.remove('hidden');

    try {
        const response = await fetch(`${API_URL}/api/match-job`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_text: matchResumeText,
                job_description: jobDescription
            })
        });

        if (!response.ok) throw new Error('Matching failed');

        const data = await response.json();
        displayMatchResults(data.match);
        document.getElementById('matchResults').classList.remove('hidden');
        
    } catch (error) {
        console.error('Error:', error);
        alert('Job matching failed. Make sure backend is running.');
    } finally {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }
});

function displayMatchResults(match) {
    document.getElementById('matchScoreDisplay').textContent = match.matchScore;
    
    document.getElementById('matchedSkillsDisplay').innerHTML = match.matchedSkills.map(skill => `
        <div class="flex items-center gap-2 text-green-700">
            <i class="fas fa-check-circle"></i>
            <span>${skill}</span>
        </div>
    `).join('');
    
    document.getElementById('missingSkillsDisplay').innerHTML = match.missingSkills.map(skill => `
        <div class="flex items-center gap-2 text-red-700">
            <i class="fas fa-times-circle"></i>
            <span>${skill}</span>
        </div>
    `).join('');
    
    document.getElementById('recommendationsDisplay').innerHTML = match.recommendations.map((rec, idx) => `
        <div class="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
            <p class="font-medium text-gray-900">${idx + 1}. ${rec}</p>
        </div>
    `).join('');
    
    document.getElementById('actionItemsDisplay').innerHTML = match.actionItems.map(action => `
        <div class="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
            <i class="fas fa-tasks text-blue-600 mt-1"></i>
            <span class="text-gray-800">${action}</span>
        </div>
    `).join('');
}