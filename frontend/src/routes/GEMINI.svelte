<script>
    import { fetchMyQuestionsGemini, makeGeminiText, sendPromptGemini } from "../lib/auth";
    import { questions, gemini_response, is_loading, is_loading2 } from "../lib/store";
    import { onMount, onDestroy } from "svelte";
    import { link, push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import { marked } from "marked";

    let prompt = '';

    let categories = [
        "지원 동기",
        "입사 후 포부",
        "성장 과정",
        "성격의 장단점",
        "직무 역량",
        "사회 이슈",
        "극복 경험",
        "협업 경험",
        "자유 양식",
        "기타(취미 또는 특기)"
    ]
    
    let selected;
    let category = '';

    let extractedKeywords = [];
    let selectedKeywords = [];
    let generatedText = '';
    let renderHTML = '';

    let loadingText = 'Loading';
    let interval1;
    let interval2;

    function startLoadingAnimation() {
        interval1 = setInterval(() => {
            if (loadingText === 'Loading...') {
                loadingText = 'Loading'
            } else {
                loadingText += '.'
            }
        }, 500);
    }
    
    function startLoadingAnimation2() {
        interval2 = setInterval(() => {
            if (loadingText === 'Loading...') {
                loadingText = 'Loading';
            } else {
                loadingText += '.';
            }
        }, 500);
    }

    onDestroy(() => {
        clearInterval(interval1, interval2);
    })

    $: if ($is_loading) {
        startLoadingAnimation();
    } else {
        loadingText = 'Loading';
        clearInterval(interval1);
    }

    $: if ($is_loading2) {
        startLoadingAnimation2();
    } else {
        loadingText = 'Loading';
        clearInterval(interval2);
    }

    function extractBoldKeywords(text) {
        const regex = /(?:-|\d+\.)\s*\*\*(.*?)\*\*/g;  // "-" 또는 "숫자."로 시작하고 "**"로 감싸진 항목을 추출
        const regex2 = /\*\*(.*?)\*\*/g; // "**"로 감싸진 텍스트를 우선적으로 추출
        const regex3 = /(?:-|\d+\.)\s*(.*?)(?:\r?\n|$)/g;  // "-" 또는 "숫자."로 시작하는 항목을 추출

        let matches;
        let keywords = [];

        // "-" 또는 "숫자."로 시작하면서 "**"로 감싸진 키워드 추출
        while ((matches = regex.exec(text)) !== null) {
            const keyword = matches[1].trim();
            if (keyword) {
                keywords.push(keyword);
            }
        }
        
        // "**"로 감싸진 키워드 추출 (위의 정규 표현식으로 누락된 경우를 대비)
        while ((matches = regex2.exec(text)) !== null) {
            const keyword = matches[1].trim();
            if (keyword && !keywords.includes(keyword)) {
                keywords.push(keyword);
            }
        }

        // "-" 또는 "숫자."로 시작하는 항목을 추출하여 키워드로 활용
        while ((matches = regex3.exec(text)) !== null) {
            const keyword = matches[1].trim();
            if (keyword && !keywords.includes(keyword)) {
                keywords.push(keyword);
            }
        }

        console.log('Extracted Keywords:', keywords);  // 추출된 키워드 확인 로그
        return keywords;
    }

    async function handleSendPrompt() {
        if (prompt.trim() === '' || category.trim() === '') {
            alert('프롬프트와 카테고리를 모두 입력하세요.');
            return;
        }
        try {
            const gptResponse = await sendPromptGemini(prompt, category);

            const answerText = gptResponse.answer || '';
            extractedKeywords = extractBoldKeywords(answerText);

            extractedKeywords = [...extractKeywords];

            if (extractKeywords.length === 0) {
                console.warn('No Keywords extracted')
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            handleSendPrompt();
        }
    }

    function toggleKeywordSelection(keyword) {
        if (selectedKeywords.includes(keyword)) {
            selectedKeywords = selectedKeywords.filter(kw => kw !== keyword);
        } else {
            selectedKeywords.push(keyword);
        }

        // 상태 업데이트를 즉시 반영
        selectedKeywords = [...selectedKeywords];
    }
    async function generateGeminiText() {
        if (selectedKeywords.length > 0) {
            try {
                const geminiResponse = await makeGeminiText(prompt, selectedKeywords);
                generatedText = geminiResponse.text;

                renderHTML = marked(generatedText);

                generatedText = generatedText;
                renderHTML = renderHTML;
            } catch (error) {
                console.error('Error:', error);
            }
        }
    }

    function copyToClipboard() {
        if (generatedText.trim() !== '') {
            navigator.clipboard.writeText(generatedText)
                .then(() => {
                    alert('텍스트가 클립보드에 복사되었습니다.');
                })
                .catch(err => {
                    console.error('텍스트 복사 실패: ', err);
                })
        }
    }


    onMount(async () => {
        if (localStorage.getItem('access_token')) {
            try {
                // await fetchMyQuestions();
            } catch (error) {
                console.error('Failed to fetch questions:', error.message);
            }
        }
    });
</script>

<div class="container">
    <div class="input-and-keywords">
        <div class="input-group">
            <select 
                class="form-select"
                bind:value={category}
            >
                <option disabled selected value="">입력란 선택</option>
                {#each categories as cat}
                    <option value={cat}>{cat}</option>
                {/each}
            </select>
            <textarea 
                class="form-control"
                placeholder="질문을 입력하세요."
                bind:value={prompt}
                on:keydown={handleKeyPress}
            />
            <button class="btn" on:click={handleSendPrompt}>추출하기</button>
        </div>

        <div class="keyword-box">
            {#if $is_loading}
                <div class="mx-auto d-flex justify-content-center">
                    <span class="navbar-text loading-animation">
                        {loadingText}
                    </span>
                </div>
            {/if}
            {#each extractedKeywords as keyword}
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div
                    class="keyword {selectedKeywords.includes(keyword) ? 'selected' : ''}"
                    on:click={() => toggleKeywordSelection(keyword)}
                >
                    {keyword}
                    <input
                        type="checkbox"
                        class="keyword-checkbox"
                        checked={selectedKeywords.includes(keyword)}
                        on:change={() => toggleKeywordSelection(keyword)}
                    />
                </div>
            {/each}
        </div>
    </div>

    <div class="selected-keywords-and-action">
        <div class="selected-keywords">
            {#each selectedKeywords as keyword}
                <div class="keyword selected">{keyword}</div>
            {/each}
        </div>

        <div class="action-buttons">
            <button class="btn-success" on:click={generateGeminiText}>생성하기</button>
        </div>
    </div>

    <div class="generated-text-area">
        {#if $is_loading2}
            <div class="mx-auto d-flex justify-content-center">
                <span class="navbar-text loading-animation">
                    {loadingText}
                </span>
            </div>
        {/if}
        {#if renderHTML}
            {@html renderHTML}
        {/if}
    </div>
    <button class="btn-copy" on:click={copyToClipboard}>복사하기</button>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin: 0 auto;
    }

    .input-and-keywords {
        display: flex;
        justify-content: space-between;
        width: 100%;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .input-group {
        display: flex;
        flex-direction: column;
        position: relative;
        width: 70%;
        gap: 10px;
    }

    .form-select {
        margin-bottom: 10px;
        width: 200px;
    }

    .form-control {
        width: 100%;
        height: 500px;
        padding: 15px;
        font-size: 1.2em;
        border-radius: 10px !important;
        border: 2px solid #d1d1e9;
        margin-bottom: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        resize: none;
    }

    .btn {
        position: absolute;
        bottom: 20px;
        right: 20px;
        background-color: #b69dfa;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 1.2em;
        border-radius: 10px !important;
        cursor: pointer;
        transition: background-color 0.3s;
        z-index: 10;
    }

    .btn:hover {
        background-color: #5a4bcf;
    }

    .keyword-box {
        margin-top: 58px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 28%;
        height: 500px;
        overflow-y: auto;
        border: 2px solid #d1d1e9;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }

    .keyword {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 15px;
        border: 2px;
        border-radius: 25px;
        font-size: 1em;
        transition: background-color 0.3s, color 0.3s;
    }

    .keyword.selected {
        background-color: #6c5ce7;
        color: white;
    }

    .keyword-checkbox {
        margin-left: 10px;
        cursor: pointer;
    }

    .selected-keywords-and-action {
        display: flex;
        align-items: center;
        gap: 20px;
        width: 100%;
        margin-top: 20px;
    }

    .selected-keywords {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        width: 80%;
    }

    button.btn-success {
        background-color: #00b894;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 1.2em;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s;
        width: 150px;
        margin-left: 150px;
    }

    button.btn-success:hover {
        background-color: #00a684;
    }

    .generated-text-area {
        margin-top: 20px;
        padding: 25px;
        background-color: #fafafa;
        border-radius: 15px;
        width: 100%;
        border: 2px solid #e0e0e0;
        font-size: 1.1em;
        line-height: 1.5em;
        box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
    }

    button.btn-copy {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 1.2em;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s;
        width: 150px;
        margin-top: 10px;
        margin-left: 1143px;
    }

    button.btn-copy:hover {
        background-color: #2980b9;
    }
</style>