// 图表实例
let comparisonChart = null;
// 全局配置
let currentConfig = null;
// 全局统计数据
let currentTheoretical = null;
let currentEmpirical = null;

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    initChart();
    loadConfig();
    loadStatistics();
});

// 加载配置
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        
        if (data.success) {
            currentConfig = data.config;
            updateProbabilityDisplay(currentConfig);
        }
    } catch (error) {
        console.error('加载配置失败:', error);
    }
}

// 动态更新概率显示
function updateProbabilityDisplay(config) {
    const probGrid = document.querySelector('.probability-grid');
    probGrid.innerHTML = '';
    
    const rarities = Object.keys(config.base_probabilities);
    rarities.forEach(rarity => {
        const prob = config.base_probabilities[rarity];
        const card = document.createElement('div');
        card.className = `prob-card ${rarity.toLowerCase().replace(/[^a-z0-9]/g, '-')}`;
        card.innerHTML = `
            <div class="rarity-label">${rarity}</div>
            <div class="prob-value">${(prob * 100).toFixed(2)}%</div>
        `;
        probGrid.appendChild(card);
    });
}

// 初始化图表
function initChart() {
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['期望抽数', '标准差', '期望回报/100', '回报标准差/100'],
            datasets: [
                {
                    label: '理论值',
                    data: [0, 0, 0, 0],
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                },
                {
                    label: '实际值',
                    data: [0, 0, 0, 0],
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(1);
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: '抽到UP最高稀有度的统计对比',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            const value = context.parsed.y;
                            // 回报相关数据需要乘以100还原
                            if (context.dataIndex >= 2) {
                                label += (value * 100).toFixed(2);
                            } else {
                                label += value.toFixed(2);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}

// 单抽
async function singleDraw() {
    try {
        const response = await fetch('/api/single_draw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySingleResult(data.result);
            updateStatistics(data);
        }
    } catch (error) {
        console.error('抽卡失败:', error);
        alert('抽卡失败，请重试');
    }
}

// 十连抽
async function multiDraw() {
    try {
        const response = await fetch('/api/multi_draw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ count: 10 })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayMultiResults(data.results);
            updateStatistics(data);
        }
    } catch (error) {
        console.error('抽卡失败:', error);
        alert('抽卡失败，请重试');
    }
}

// 显示单抽结果
function displaySingleResult(result) {
    const resultDisplay = document.getElementById('resultDisplay');
    resultDisplay.innerHTML = '';
    
    const card = createResultCard(result);
    resultDisplay.appendChild(card);
    
    // 显示回报信息
    if (result.reward > 0) {
        const rewardInfo = document.createElement('div');
        rewardInfo.className = 'reward-info';
        rewardInfo.textContent = `+${result.reward} 回报`;
        resultDisplay.appendChild(rewardInfo);
    }
}

// 显示多抽结果
function displayMultiResults(results) {
    const resultDisplay = document.getElementById('resultDisplay');
    resultDisplay.innerHTML = '';
    
    results.forEach((result, index) => {
        setTimeout(() => {
            const card = createResultCard(result);
            resultDisplay.appendChild(card);
        }, index * 100); // 每个卡片延迟100ms出现
    });
}

// 创建结果卡片
function createResultCard(result) {
    const card = document.createElement('div');
    let className = result.rarity.toLowerCase().replace(/[^a-z0-9]/g, '-');
    let text = result.rarity;
    
    // 如果是最高稀有度，显示是否UP
    const topRarity = currentConfig ? currentConfig.rate_up_rarity : null;
    if (topRarity && result.rarity === topRarity) {
        if (result.is_rate_up) {
            text += ' (UP)';
            className += '-up';
        } else {
            text += ' (歪)';
            className += '-non-up';
        }
    }
    
    card.className = `result-card ${className}`;
    card.textContent = text;
    return card;
}

// 更新统计信息
function updateStatistics(data) {
    // 更新总次数和总回报
    document.getElementById('totalDraws').textContent = data.total_draws;
    document.getElementById('totalRewards').textContent = data.total_rewards || 0;
    
    // 如果有完整统计数据
    if (data.statistics && data.statistics.rarity_stats) {
        const rarityStats = data.statistics.rarity_stats;
        const topRarityStats = data.statistics.top_rarity_stats;
        const pityInfo = data.statistics.pity_info;
        
        // 动态更新稀有度统计显示
        updateRarityStatsDisplay(rarityStats, topRarityStats);
        
        // 更新保底状态
        if (pityInfo) {
            const topRarityName = pityInfo.top_rarity_name || '最高稀有度';
            
            document.getElementById('drawsSinceSsr').textContent = pityInfo.draws_since_top_rarity + ' 抽';
            document.querySelector('.pity-card:nth-child(1) .pity-label').textContent = `距上次${topRarityName}`;
            
            document.getElementById('currentSsrProb').textContent = (pityInfo.current_top_rarity_prob * 100).toFixed(2) + '%';
            document.querySelector('.pity-card:nth-child(2) .pity-label').textContent = `当前${topRarityName}概率`;
            
            if (pityInfo.draws_until_hard_pity !== null) {
                document.getElementById('untilHardPity').textContent = pityInfo.draws_until_hard_pity + ' 抽';
            }
            
            if (pityInfo.draws_until_big_pity !== null) {
                document.getElementById('untilBigPity').textContent = pityInfo.draws_until_big_pity + ' 抽';
            }
            
            // 显示或隐藏保底UP提示
            const guaranteedCard = document.getElementById('guaranteedCard');
            if (pityInfo.is_guaranteed_rate_up) {
                guaranteedCard.style.display = 'block';
            } else {
                guaranteedCard.style.display = 'none';
            }
        }
    }
    
    // 更新历史记录
    if (data.history) {
        updateHistory(data.history);
    }
}

// 动态更新稀有度统计显示
function updateRarityStatsDisplay(rarityStats, topRarityStats) {
    const statsGrid = document.querySelector('.stats-grid');
    
    // 保留前两个卡片（总抽卡次数、总回报）
    const fixedCards = Array.from(statsGrid.children).slice(0, 2);
    statsGrid.innerHTML = '';
    fixedCards.forEach(card => statsGrid.appendChild(card));
    
    // 添加最高稀有度统计
    if (topRarityStats && topRarityStats.rarity_name) {
        const topRarity = topRarityStats.rarity_name;
        const topStat = rarityStats[topRarity];
        
        // 最高稀有度总数
        const topCard = document.createElement('div');
        topCard.className = 'stat-card ssr';
        topCard.innerHTML = `
            <div class="stat-label">${topRarity}总数</div>
            <div class="stat-value">${topStat.count} (${(topStat.probability * 100).toFixed(2)}%)</div>
        `;
        statsGrid.appendChild(topCard);
        
        // UP统计
        const upCard = document.createElement('div');
        upCard.className = 'stat-card ssr-up';
        upCard.innerHTML = `
            <div class="stat-label">UP ${topRarity}</div>
            <div class="stat-value">${topRarityStats.rate_up}</div>
        `;
        statsGrid.appendChild(upCard);
        
        // 歪的统计
        const nonUpCard = document.createElement('div');
        nonUpCard.className = 'stat-card ssr-non-up';
        nonUpCard.innerHTML = `
            <div class="stat-label">歪的${topRarity}</div>
            <div class="stat-value">${topRarityStats.non_rate_up}</div>
        `;
        statsGrid.appendChild(nonUpCard);
    }
    
    // 添加其他稀有度统计
    Object.keys(rarityStats).forEach(rarity => {
        if (topRarityStats && rarity === topRarityStats.rarity_name) {
            return; // 跳过最高稀有度（已添加）
        }
        
        const stat = rarityStats[rarity];
        const card = document.createElement('div');
        card.className = `stat-card ${rarity.toLowerCase().replace(/[^a-z0-9]/g, '-')}`;
        card.innerHTML = `
            <div class="stat-label">${rarity}</div>
            <div class="stat-value">${stat.count} (${(stat.probability * 100).toFixed(2)}%)</div>
        `;
        statsGrid.appendChild(card);
    });
}

// 更新对比图表
function updateComparisonChart() {
    if (!comparisonChart) return;
    
    // 如果有理论和实际统计数据，更新图表
    if (currentTheoretical && currentEmpirical && currentEmpirical.sample_size > 0) {
        const theoreticalData = [
            currentTheoretical.expected_draws_for_up,
            currentTheoretical.std_draws,
            currentTheoretical.expected_total_reward / 100,  // 除以100以便在同一图表显示
            currentTheoretical.std_total_reward / 100
        ];
        
        const empiricalData = [
            currentEmpirical.expected_draws_for_up,
            currentEmpirical.std_draws,
            currentEmpirical.expected_total_reward / 100,
            currentEmpirical.std_total_reward / 100
        ];
        
        comparisonChart.data.datasets[0].data = theoreticalData;
        comparisonChart.data.datasets[1].data = empiricalData;
        comparisonChart.update();
    }
}

// 显示期望抽数图表
function showExpectedDrawsChart() {
    if (!comparisonChart || !currentTheoretical || !currentEmpirical) return;
    
    comparisonChart.data.labels = ['期望抽数'];
    comparisonChart.data.datasets[0].data = [currentTheoretical.expected_draws_for_up];
    comparisonChart.data.datasets[1].data = [currentEmpirical.expected_draws_for_up || 0];
    comparisonChart.options.plugins.title.text = '期望抽数对比';
    comparisonChart.update();
}

// 显示期望回报图表
function showRewardsChart() {
    if (!comparisonChart || !currentTheoretical || !currentEmpirical) return;
    
    comparisonChart.data.labels = ['期望总回报'];
    comparisonChart.data.datasets[0].data = [currentTheoretical.expected_total_reward];
    comparisonChart.data.datasets[1].data = [currentEmpirical.expected_total_reward || 0];
    comparisonChart.options.plugins.title.text = '期望总回报对比';
    comparisonChart.update();
}

// 显示标准差图表
function showVarianceChart() {
    if (!comparisonChart || !currentTheoretical || !currentEmpirical) return;
    
    comparisonChart.data.labels = ['抽数标准差', '回报标准差/100'];
    comparisonChart.data.datasets[0].data = [
        currentTheoretical.std_draws,
        currentTheoretical.std_total_reward / 100
    ];
    comparisonChart.data.datasets[1].data = [
        currentEmpirical.std_draws || 0,
        (currentEmpirical.std_total_reward || 0) / 100
    ];
    comparisonChart.options.plugins.title.text = '标准差对比';
    comparisonChart.update();
}

// 更新历史记录
function updateHistory(history) {
    const historyDisplay = document.getElementById('historyDisplay');
    historyDisplay.innerHTML = '';
    
    if (history.length === 0) {
        historyDisplay.innerHTML = '<p class="placeholder">暂无记录</p>';
        return;
    }
    
    // 倒序显示（最新的在前面）
    const reversedHistory = [...history].reverse();
    const topRarity = currentConfig ? currentConfig.rate_up_rarity : null;
    
    reversedHistory.forEach(result => {
        const item = document.createElement('div');
        let className = result.rarity.toLowerCase().replace(/[^a-z0-9]/g, '-');
        let text = result.rarity;
        
        // 如果是最高稀有度，显示是否UP
        if (topRarity && result.rarity === topRarity) {
            if (result.is_rate_up) {
                text += '(UP)';
                className += '-up';
            } else {
                text += '(歪)';
                className += '-non-up';
            }
        }
        
        item.className = `history-item ${className}`;
        item.textContent = text;
        item.title = `回报: ${result.reward}`;
        historyDisplay.appendChild(item);
    });
}

// 加载统计信息
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        if (data.success) {
            updateStatistics(data);
        }
    } catch (error) {
        console.error('加载统计信息失败:', error);
    }
}

// 重置统计
async function resetStats() {
    if (!confirm('确定要重置所有统计信息吗？')) {
        return;
    }
    
    try {
        const response = await fetch('/api/reset', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 清空显示
            document.getElementById('resultDisplay').innerHTML = '<p class="placeholder">点击按钮开始抽卡</p>';
            document.getElementById('historyDisplay').innerHTML = '<p class="placeholder">暂无记录</p>';
            
            // 重置统计
            document.getElementById('totalDraws').textContent = '0';
            document.getElementById('totalRewards').textContent = '0';
            document.getElementById('ssrCount').textContent = '0 (0.00%)';
            document.getElementById('ssrUpCount').textContent = '0';
            document.getElementById('ssrNonUpCount').textContent = '0';
            document.getElementById('srCount').textContent = '0 (0.00%)';
            document.getElementById('rCount').textContent = '0 (0.00%)';
            document.getElementById('nCount').textContent = '0 (0.00%)';
            
            // 重置保底状态
            document.getElementById('drawsSinceSsr').textContent = '0 抽';
            document.getElementById('currentSsrProb').textContent = '0.60%';
            document.getElementById('untilHardPity').textContent = '90 抽';
            document.getElementById('untilBigPity').textContent = '180 抽';
            document.getElementById('guaranteedCard').style.display = 'none';
            
            // 重置图表
            currentTheoretical = null;
            currentEmpirical = null;
            if (comparisonChart) {
                comparisonChart.data.datasets[0].data = [0, 0, 0, 0];
                comparisonChart.data.datasets[1].data = [0, 0, 0, 0];
                comparisonChart.update();
            }
            
            alert('统计已重置');
        }
    } catch (error) {
        console.error('重置失败:', error);
        alert('重置失败，请重试');
    }
}

// 运行模拟
async function runSimulation() {
    const countInput = document.getElementById('simulationCount');
    const count = parseInt(countInput.value);
    
    if (isNaN(count) || count < 1000) {
        alert('请输入至少1000次模拟');
        return;
    }
    
    if (count > 10000000) {
        alert('模拟次数最多为1000万次');
        return;
    }
    
    // 显示加载状态
    const resultDiv = document.getElementById('simulationResult');
    resultDiv.innerHTML = '<div class="loading"></div> 模拟中，请稍候...';
    
    // 禁用按钮
    const btn = event.target;
    btn.disabled = true;
    
    try {
        const startTime = Date.now();
        
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ count: count })
        });
        
        const data = await response.json();
        const endTime = Date.now();
        const duration = ((endTime - startTime) / 1000).toFixed(2);
        
        if (data.success) {
            displaySimulationResult(data, duration);
            updateStatistics(data);
        }
    } catch (error) {
        console.error('模拟失败:', error);
        resultDiv.textContent = '模拟失败，请重试';
    } finally {
        btn.disabled = false;
    }
}

// 显示模拟结果
function displaySimulationResult(data, duration) {
    const resultDiv = document.getElementById('simulationResult');
    
    const stats = data.statistics;
    const rarityStats = stats.rarity_stats;
    const topRarityStats = stats.top_rarity_stats;
    const pityInfo = stats.pity_info;
    const theoretical = data.theoretical_stats;
    const empirical = data.empirical_stats;
    
    // 保存到全局变量用于图表更新
    currentTheoretical = theoretical;
    currentEmpirical = empirical;
    
    // 更新图表
    updateComparisonChart();
    
    let html = `<strong>═══════════════════════════════════════════════════════════════════</strong>\n`;
    html += `<strong>                          模拟完成！                              </strong>\n`;
    html += `<strong>═══════════════════════════════════════════════════════════════════</strong>\n\n`;
    
    html += `模拟次数: ${data.simulated_count.toLocaleString()}\n`;
    html += `总回报: ${data.total_rewards.toLocaleString()}\n`;
    html += `耗时: ${duration} 秒\n\n`;
    
    // 基础统计
    html += `<strong>━━━━━━━━━━━━━━━━━━━━━━━ 基础统计 ━━━━━━━━━━━━━━━━━━━━━━━</strong>\n\n`;
    html += `<strong>稀有度统计：</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `${'稀有度'.padEnd(10)} ${'基础概率'.padEnd(12)} ${'实际概率'.padEnd(12)} ${'抽取次数'.padEnd(15)}\n`;
    html += `${'─'.repeat(70)}\n`;
    
    const rarities = Object.keys(rarityStats);
    rarities.forEach(rarity => {
        const stat = rarityStats[rarity];
        const theory = (stat.base_probability * 100).toFixed(2) + '%';
        const actual = (stat.probability * 100).toFixed(2) + '%';
        const count = stat.count.toLocaleString();
        
        html += `${rarity.padEnd(10)} ${theory.padEnd(12)} ${actual.padEnd(12)} ${count.padEnd(15)}\n`;
    });
    
    const topRarityName = topRarityStats ? topRarityStats.rarity_name : '最高稀有度';
    
    html += `\n<strong>${topRarityName}详细统计：</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `总${topRarityName}数: ${topRarityStats.total}\n`;
    html += `UP ${topRarityName}: ${topRarityStats.rate_up} (${(topRarityStats.rate_up_ratio * 100).toFixed(2)}%)\n`;
    html += `歪的${topRarityName}: ${topRarityStats.non_rate_up} (${((1 - topRarityStats.rate_up_ratio) * 100).toFixed(2)}%)\n`;
    
    html += `\n<strong>当前保底状态：</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `距上次${topRarityName}: ${pityInfo.draws_since_top_rarity} 抽\n`;
    html += `当前${topRarityName}概率: ${(pityInfo.current_top_rarity_prob * 100).toFixed(2)}%\n`;
    if (pityInfo.draws_until_hard_pity !== null) {
        html += `距硬保底: ${pityInfo.draws_until_hard_pity} 抽\n`;
    }
    html += `距上次UP: ${pityInfo.draws_since_rate_up} 抽\n`;
    if (pityInfo.draws_until_big_pity !== null) {
        html += `距大保底: ${pityInfo.draws_until_big_pity} 抽\n`;
    }
    html += `是否保底UP: ${pityInfo.is_guaranteed_rate_up ? '是' : '否'}\n`;
    
    // 高级统计
    html += `\n<strong>━━━━━━━━━━━━━━━━━━━━━━━ 高级统计 ━━━━━━━━━━━━━━━━━━━━━━━</strong>\n\n`;
    html += `<strong>基于几何分布的UP ${topRarityName}统计分析：</strong>\n`;
    html += `${'═'.repeat(70)}\n\n`;
    
    // 1. 期望抽数
    html += `<strong>【1】抽到UP ${topRarityName}的期望抽数</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `理论值: ${theoretical.expected_draws_for_up.toFixed(2)} 抽\n`;
    html += `模拟值: ${empirical.expected_draws_for_up.toFixed(2)} 抽`;
    if (empirical.sample_size) {
        html += ` (基于 ${empirical.sample_size} 个UP ${topRarityName}样本)`;
    }
    html += `\n`;
    const drawsDiff = Math.abs(theoretical.expected_draws_for_up - empirical.expected_draws_for_up);
    const drawsError = (drawsDiff / theoretical.expected_draws_for_up * 100).toFixed(2);
    html += `误差: ${drawsDiff.toFixed(2)} 抽 (${drawsError}%)\n\n`;
    
    // 2. 方差和标准差
    html += `<strong>【2】抽到UP ${topRarityName}的方差与标准差</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `理论方差: ${theoretical.variance_draws.toFixed(2)}\n`;
    html += `模拟方差: ${empirical.variance_draws.toFixed(2)}\n`;
    html += `理论标准差: ${theoretical.std_draws.toFixed(2)} 抽\n`;
    html += `模拟标准差: ${empirical.std_draws.toFixed(2)} 抽\n`;
    const stdDiff = Math.abs(theoretical.std_draws - empirical.std_draws);
    const stdError = theoretical.std_draws > 0 ? (stdDiff / theoretical.std_draws * 100).toFixed(2) : '0.00';
    html += `标准差误差: ${stdDiff.toFixed(2)} (${stdError}%)\n\n`;
    
    // 3. 期望回报
    html += `<strong>【3】抽到UP ${topRarityName}的期望回报</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `单抽期望回报: ${theoretical.expected_reward_per_draw.toFixed(2)}\n`;
    html += `理论总回报: ${theoretical.expected_total_reward.toFixed(2)}\n`;
    html += `模拟总回报: ${empirical.expected_total_reward.toFixed(2)}\n`;
    const rewardDiff = Math.abs(theoretical.expected_total_reward - empirical.expected_total_reward);
    const rewardError = theoretical.expected_total_reward > 0 ? 
        (rewardDiff / theoretical.expected_total_reward * 100).toFixed(2) : '0.00';
    html += `误差: ${rewardDiff.toFixed(2)} (${rewardError}%)\n\n`;
    
    // 4. 回报方差
    html += `<strong>【4】回报的方差与标准差</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `理论回报方差: ${theoretical.variance_total_reward.toFixed(2)}\n`;
    html += `模拟回报方差: ${empirical.variance_total_reward.toFixed(2)}\n`;
    html += `理论回报标准差: ${theoretical.std_total_reward.toFixed(2)}\n`;
    html += `模拟回报标准差: ${empirical.std_total_reward.toFixed(2)}\n`;
    const rewardStdDiff = Math.abs(theoretical.std_total_reward - empirical.std_total_reward);
    const rewardStdError = theoretical.std_total_reward > 0 ? 
        (rewardStdDiff / theoretical.std_total_reward * 100).toFixed(2) : '0.00';
    html += `标准差误差: ${rewardStdDiff.toFixed(2)} (${rewardStdError}%)\n\n`;
    
    // 统计解释
    html += `<strong>统计说明：</strong>\n`;
    html += `${'─'.repeat(70)}\n`;
    html += `• 期望值：抽到一个UP ${topRarityName}平均需要的抽数\n`;
    html += `• 方差/标准差：衡量抽数的波动程度，越小越稳定\n`;
    html += `• 期望回报：抽到一个UP ${topRarityName}过程中平均获得的总回报\n`;
    html += `• 回报方差：衡量回报的波动程度\n`;
    html += `• 理论值：基于概率模型和保底机制的数学计算\n`;
    html += `• 模拟值：基于实际抽卡历史数据的统计结果\n\n`;
    
    html += `<strong>═══════════════════════════════════════════════════════════════════</strong>\n`;
    
    resultDiv.innerHTML = `<pre>${html}</pre>`;
}

// 键盘快捷键
document.addEventListener('keydown', function(event) {
    if (event.target.tagName === 'INPUT') return;
    
    switch(event.key) {
        case '1':
            singleDraw();
            break;
        case '0':
            multiDraw();
            break;
        case 'r':
        case 'R':
            if (event.ctrlKey) {
                event.preventDefault();
                resetStats();
            }
            break;
    }
});
