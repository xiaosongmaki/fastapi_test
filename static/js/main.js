document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate-btn');
    const storyContent = document.getElementById('story-content');
    const elementsContent = document.getElementById('elements-content');

    // 加载故事元素
    async function loadStoryElements() {
        try {
            const response = await fetch('/api/elements');
            const elements = await response.json();
            
            let html = '';
            for (const [category, items] of Object.entries(elements)) {
                html += `
                    <div class="element-category">
                        <h5>${categoryToTitle(category)}</h5>
                        <div>
                            ${items.map(item => `<span class="element-item">${item}</span>`).join('')}
                        </div>
                    </div>
                `;
            }
            elementsContent.innerHTML = html;
        } catch (error) {
            console.error('加载故事元素失败:', error);
        }
    }

    // 生成新故事
    async function generateStory() {
        try {
            generateBtn.disabled = true;
            generateBtn.innerHTML = '生成中...';
            
            const response = await fetch('/api/story');
            const data = await response.json();
            
            if (data.status === 'success') {
                storyContent.innerHTML = `
                    <div class="fade-in">
                        <p>${data.data.story.split('\n').join('</p><p>')}</p>
                    </div>
                `;
            } else {
                throw new Error(data.message || '生成故事失败');
            }
        } catch (error) {
            storyContent.innerHTML = `
                <div class="alert alert-danger">
                    生成故事时发生错误: ${error.message}
                </div>
            `;
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '生成新故事';
        }
    }

    // 辅助函数：转换类别名称
    function categoryToTitle(category) {
        const titles = {
            scenes: '场景',
            characters: '角色',
            actions: '动作',
            emotions: '情绪'
        };
        return titles[category] || category;
    }

    // 事件监听
    generateBtn.addEventListener('click', generateStory);
    
    // 初始加载
    loadStoryElements();
});
