const API_URL = 'http://localhost:8000';

let currentAnalysis = null;

// File upload handling
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

// Analyze button
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('resumeFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file first');
        return;
    }

    // Show loading
    document.getElementById('loadingOverlay').classList.remove('hidden');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const data = await response.json();
        currentAnalysis = data.analysis;
        
        displayResults(currentAnalysis);
        
        // Hide upload, show results
        document.getElementById('uploadSection').classList.add('hidden');
        document.getElementById('resultsSection').classList.remove('hidden');
        
    } catch (error) {
        console.error('Error:', error);
        alert('Analysis failed. Make sure the backend is running.');
    } finally {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }
});

// Display results
function displayResults(analysis) {
    // Score cards
    const scoreCards = document.getElementById('scoreCards');
    const scores = [
        { label: 'Overall Score', value: analysis.overallScore },
        { label: 'ATS Score', value: analysis.atsScore },
        { label: 'Content Quality', value: analysis.contentScore },
        { label: 'Format Score', value: analysis.formatScore }
    ];

    scoreCards.innerHTML = scores.map(score => {
        const colorClass = score.value >= 80 ? 'border-green-500 bg-green-50 text-green-700' : 
                          score.value >= 60 ? 'border-yellow-500 bg-yellow-50 text-yellow-700' : 
                          'border-red-500 bg-red-50 text-red-700';
        return `
            <div class="bg-white rounded-xl shadow-lg p-6 border-2 ${colorClass}">
                <p class="text-sm font-medium mb-2">${score.label}</p>
                <p class="text-5xl font-bold">${score.value}</p>
                <p class="text-xs mt-1">out of 100</p>
            </div>
        `;
    }).join('');

    // Detailed analysis
    const detailedAnalysis = document.getElementById('detailedAnalysis');
    detailedAnalysis.innerHTML = `
        <!-- Section Analysis -->
        <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4">
                <i class="fas fa-file-alt text-blue-600 mr-2"></i>
                Section-by-Section Analysis
            </h3>
            <div class="space-y-3">
                ${Object.entries(analysis.sections).map(([key, section]) => `
                    <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border">
                        <div class="flex items-center gap-3 flex-1">
                            <i class="fas fa-${section.status === 'good' ? 'check-circle text-green-600' : 
                                               section.status === 'warning' ? 'exclamation-circle text-yellow-600' : 
                                               'times-circle text-red-600'}"></i>
                            <div>
                                <p class="font-semibold text-gray-900 capitalize">${key}</p>
                                <p class="text-sm text-gray-600">${section.message}</p>
                            </div>
                        </div>
                        <div class="text-2xl font-bold text-gray-900">${section.score}</div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- Strengths and Improvements -->
        <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-green-600 mb-4">
                    <i class="fas fa-check-circle mr-2"></i>Strengths
                </h3>
                <ul class="space-y-2">
                    ${analysis.strengths.map(strength => `
                        <li class="flex items-start gap-2 text-gray-700">
                            <i class="fas fa-check text-green-600 mt-1"></i>
                            <span>${strength}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-yellow-600 mb-4">
                    <i class="fas fa-exclamation-triangle mr-2"></i>Improvements
                </h3>
                <ul class="space-y-2">
                    ${analysis.improvements.map(improvement => `
                        <li class="flex items-start gap-2 text-gray-700">
                            <i class="fas fa-arrow-right text-yellow-600 mt-1"></i>
                            <span>${improvement}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        </div>

        <!-- Skills -->
        <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-blue-600 mb-4">Found Skills</h3>
                <div class="flex flex-wrap gap-2">
                    ${analysis.extractedSkills.map(skill => `
                        <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                            ${skill}
                        </span>
                    `).join('')}
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-red-600 mb-4">Missing Keywords</h3>
                <div class="flex flex-wrap gap-2">
                    ${analysis.missingKeywords.map(keyword => `
                        <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-medium">
                            ${keyword}
                        </span>
                    `).join('')}
                </div>
            </div>
        </div>

        ${analysis.detailedFeedback ? `
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-900 mb-4">Detailed Feedback</h3>
                <p class="text-gray-700 leading-relaxed">${analysis.detailedFeedback}</p>
            </div>
        ` : ''}
    `;
}

// New analysis button
document.getElementById('newAnalysisBtn').addEventListener('click', () => {
    document.getElementById('uploadSection').classList.remove('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('resumeFile').value = '';
    document.getElementById('fileInfo').classList.add('hidden');
    currentAnalysis = null;
});

// Download report (placeholder)
document.getElementById('downloadBtn').addEventListener('click', () => {
    alert('Download feature coming soon! For now, take a screenshot of your results.');
});