document.addEventListener('DOMContentLoaded', () => {
    
    // Theme Toggle Logic
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            htmlElement.setAttribute('data-bs-theme', newTheme);
            themeToggleBtn.innerHTML = newTheme === 'dark' ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
        });
    }

    // Dashboard Calculator Logic
    const calcForm = document.getElementById('calculator-form');
    let analysisChart = null;

    if (calcForm) {
        calcForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const city = document.getElementById('city').value;
            const farmSize = document.getElementById('farm-size').value;
            const soilMoisture = document.getElementById('soil-moisture').value;
            const btn = document.getElementById('calc-btn');
            
            const weatherLoading = document.getElementById('weather-loading');
            const weatherContent = document.getElementById('weather-content');
            const resultsSection = document.getElementById('results-section');
            
            // UI State
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
            weatherContent.classList.add('opacity-50');
            weatherLoading.classList.remove('d-none');
            
            try {
                // 1. Fetch Weather
                const weatherRes = await fetch('/api/weather', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ city: city })
                });
                const weatherData = await weatherRes.json();
                
                if (!weatherData.success) {
                    alert(weatherData.message);
                    throw new Error(weatherData.message);
                }
                
                const w = weatherData.data;
                document.getElementById('w-temp').innerText = `${w.temp} °C`;
                document.getElementById('w-humidity').innerText = `${w.humidity} %`;
                document.getElementById('w-wind').innerText = `${w.wind_speed} m/s`;
                document.getElementById('w-clouds').innerText = `${w.clouds} %`;
                document.getElementById('w-desc').innerText = w.description;
                
                weatherLoading.classList.add('d-none');
                weatherContent.classList.remove('opacity-50');
                
                if (weatherData.warning) {
                    console.warn(weatherData.warning);
                }

                // 2. Calculate Water & Recommend Crops
                const calcRes = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        city: city,
                        farm_size: farmSize,
                        soil_moisture: soilMoisture,
                        temperature: w.temp,
                        humidity: w.humidity
                    })
                });
                const calcData = await calcRes.json();
                
                if (calcData.success) {
                    document.getElementById('res-water').innerText = calcData.water_required;
                    document.getElementById('res-tips').innerText = calcData.efficiency_tips;
                    
                    const cropList = document.getElementById('res-crops');
                    cropList.innerHTML = '';
                    
                    if (calcData.recommended_crops.length > 0) {
                        calcData.recommended_crops.forEach(crop => {
                            cropList.innerHTML += `<li class="list-group-item bg-transparent text-success fw-bold border-success border-opacity-25"><i class="fa-solid fa-check me-2"></i>${crop.name}</li>`;
                        });
                    } else {
                        cropList.innerHTML = `<li class="list-group-item bg-transparent text-muted border-0">No perfect matches. Consult local experts.</li>`;
                    }
                    
                    resultsSection.classList.remove('d-none');
                    
                    // 3. Draw Chart
                    drawChart(w.temp, w.humidity, soilMoisture, calcData.water_required);
                }
                
            } catch (err) {
                console.error(err);
                weatherLoading.classList.add('d-none');
                weatherContent.classList.remove('opacity-50');
            } finally {
                btn.disabled = false;
                btn.innerHTML = 'Analyze & Calculate';
            }
        });
    }

    function drawChart(temp, humidity, soil, water) {
        const ctx = document.getElementById('analysisChart').getContext('2d');
        
        if (analysisChart) {
            analysisChart.destroy();
        }
        
        analysisChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Temperature (°C)', 'Humidity (%)', 'Soil Moisture (%)', 'Water Req (scaled)'],
                datasets: [{
                    label: 'Current Metrics',
                    data: [temp, humidity, soil, water > 100 ? 100 : water],
                    backgroundColor: [
                        'rgba(245, 158, 11, 0.6)',
                        'rgba(59, 130, 246, 0.6)',
                        'rgba(16, 185, 129, 0.6)',
                        'rgba(14, 165, 233, 0.6)'
                    ],
                    borderColor: [
                        'rgba(245, 158, 11, 1)',
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(14, 165, 233, 1)'
                    ],
                    borderWidth: 1,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#cbd5e1' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#cbd5e1' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // PDF Export Logic
    const pdfBtn = document.getElementById('export-pdf-btn');
    if (pdfBtn) {
        pdfBtn.addEventListener('click', () => {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            
            doc.setFontSize(22);
            doc.setTextColor(16, 185, 129);
            doc.text("Smart Water Irrigator - Report", 20, 20);
            
            doc.setFontSize(12);
            doc.setTextColor(50, 50, 50);
            
            const city = document.getElementById('city').value || 'N/A';
            const water = document.getElementById('res-water').innerText || '0';
            const temp = document.getElementById('w-temp').innerText || 'N/A';
            
            doc.text(`Date: ${new Date().toLocaleDateString()}`, 20, 40);
            doc.text(`Location: ${city}`, 20, 50);
            doc.text(`Temperature: ${temp}`, 20, 60);
            doc.text(`Irrigation Required: ${water} Liters`, 20, 70);
            
            doc.text("Efficiency Tips:", 20, 90);
            const tips = document.getElementById('res-tips').innerText || 'None';
            doc.text(tips, 20, 100);
            
            doc.save('Irrigation_Report.pdf');
        });
    }
});
