<script>
    import { questions } from '../lib/store';
    import { fetchMyQuestions, makeText, sendPrompt } from '../lib/auth.js';
    import { gpt_response, is_loading, is_loading2 } from '../lib/store';
    import { onMount, onDestroy } from 'svelte';
    import { link, push } from 'svelte-spa-router';
    import fastapi from '../lib/api';
    import { marked } from 'marked';

    let prompt = '';

    let categories = [
        "지원동기",
        "관심분야",
        "교내외 활동 및 경력",
        "성격의 장단점"
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

    // 애니메이션 초기화
    function startLoadingAnimation() {
        interval1 = setInterval(() => {
            if (loadingText === 'Loading...') {
                loadingText = 'Loading';
            } else {
                loadingText += '.';
            }
        }, 500);
    }
    
    // 애니메이션 초기화
    function startLoadingAnimation2() {
        interval2 = setInterval(() => {
            if (loadingText === 'Loading...') {
                loadingText = 'Loading';
            } else {
                loadingText += '.';
            }
        }, 500);
    }

    // 컴포넌트가 파괴될 때 애니메이션 중지
    onDestroy(() => {
        clearInterval(interval1, interval2);
    });

    // 로딩 상태가 true일 때 애니메이션 시작
    $: if ($is_loading) {
        startLoadingAnimation();
    } else {
        loadingText = 'Loading';
        clearInterval(interval1);
    }

    // 로딩 상태가 true일 때 애니메이션 시작
    $: if ($is_loading2) {
        startLoadingAnimation2();
    } else {
        loadingText = 'Loading';
        clearInterval(interval2);
    }

    // **로 감싸진 텍스트를 추출하는 함수
    function extractBoldKeywords(text) {
        const regex = /\*\*(.*?)\*\*/g;
        let matches;
        let keywords = [];
        while ((matches = regex.exec(text)) !== null) {
            keywords.push(matches[1].trim());
        }
        console.log('Extracted Keywords:', keywords);  // 추출된 키워드 확인 로그
        return keywords;
    }

    async function handleSendPrompt() {
        if (prompt.trim() === '' || category.trim() === '') {
            alert('프롬프트와 카테고리를 입력해 주세요.');
            return;
        }
        try {
            const gptResponse = await sendPrompt(prompt, category);

            // 응답에서 answer 필드를 추출하여 키워드 추출
            const answerText = gptResponse.answer || '';  // answer 필드가 존재하지 않으면 빈 문자열
            extractedKeywords = extractBoldKeywords(answerText);

            // 상태 업데이트를 즉시 반영
            extractedKeywords = [...extractedKeywords];

            if (extractedKeywords.length === 0) {
                console.warn('No keywords extracted. Check the response format or the regex.');
            }
        } catch (error) {
            console.error('Failed to send prompt:', error);
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

    async function generateText() {
        if (selectedKeywords.length > 0) {
            try {
                console.log(prompt);
                console.log('Generating text with keywords:', selectedKeywords);
                const gptResponse = await makeText(prompt, selectedKeywords);
                generatedText = gptResponse.answer;

                renderHTML = marked(generatedText);

                // 상태 업데이트를 즉시 반영
                generatedText = generatedText;
                renderHTML = renderHTML;
            } catch (error) {
                console.error('Failed to generate text:', error);
            }
        }
    }

    function delete_question(_question_id) {
        if (window.confirm("정말로 삭제하시겠습니까?")) {
            let url = "/api/question/delete"
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params,
                (json) => {
                    push('/self')
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                },
                (err_json) => {
                    error = err_json
                }
            )
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

<div class="container">
    <div class="input-and-keywords">
        <div class="input-group">
            <select
                class="form-select"
                bind:value={category}
                on:change={() => console.log(category)}
            >
                <option disabled selected value="">입력란 선택</option>
                {#each categories as cat}
                    <option value={cat}>{cat}</option>
                {/each}
            </select>
            <textarea
                class="form-control"
                placeholder="Enter your prompt"
                bind:value={prompt}
                on:keypress={handleKeyPress}
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
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            {#each extractedKeywords as keyword}
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
            <button class="btn-success" on:click={generateText}>생성하기</button>
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

<!-- <div class="table mt-4">
    <thead>
        <tr class="text-center table-dark">
            <th style="width: 50%;">질문</th>
            <th>대답</th>
            <th>수정</th>
            <th>삭제</th>
        </tr>
    </thead>
    <tbody>
        {#each $questions as question}
            <tr class="text-center">
                <td>{question.subject}</td>
                <td>{question.content}</td>
                <td>
                    <a use:link href="/question-modify/{question.id}" class="btn-sm btn-outline-secondary">
                        재질문하기
                    </a>
                </td>
                <td>
                    <button class="btn-sm btn-outline-secondary" on:click={()=> delete_question(question.id)}>
                        삭제
                    </button>
                </td>
            </tr>
        {/each}
    </tbody>
</div> -->




<!-- .table {
    width: 100%;
    margin-top: 40px;
    border-collapse: collapse;
}

thead {
    background-color: #b69dfa;
    color: white;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

tr:hover {
    background-color: #ececec;
}

.btn-sm {
    padding: 10px 15px;
    font-size: 0.9em;
    border-radius: 8px;
    margin: 5px;
}

.btn-outline-secondary {
    border: 1px solid #b69dfa;
    color: #b69dfa;
    background-color: white;
    transition: background-color 0.3s ease;
}

.btn-outline-secondary:hover {
    background-color: #b69dfa;
    color: white;
}

table tr td a.btn {
    width: 100%;
    box-sizing: border-box;
} -->


<!-- <style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }

    .input-and-keywords {
        display: flex;
        justify-content: space-between;
        width: 100%;
        max-width: 1200px;
        margin-bottom: 20px;
    }

    .input-group {
        display: flex;
        flex-direction: column;
        width: 70%;
        margin-right: 20px;
    }

    .form-control {
        width: 100%;
        height: 300px;
        padding: 15px;
        font-size: 1.2em;
        border-radius: 10px;
        border: 2px solid #d1d1e9;
        margin-bottom: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        resize: none;
    }

    .btn {
        background-color: #b69dfa;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 1.2em;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s;
        width: 150px;
        align-self: flex-end;
        margin-top: 10px;
    }

    .btn:hover {
        background-color: #5a4bcf;
    }

    .keywords-container {
        display: flex;
        gap: 20px;
        width: 100%;
        justify-content: space-between;
        align-items: flex-start;
    }

    .keyword-box {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 40%;
    }

    .keyword {
        padding: 10px 15px;
        border: 2px solid #6c5ce7;
        border-radius: 25px;
        cursor: pointer;
        background-color: #f0f0f0;
        font-size: 1em;
        transition: background-color 0.3s, color 0.3s;
    }

    .keyword.selected {
        background-color: #6c5ce7;
        color: white;
    }

    .action-buttons {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
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
        max-width: 800px;
        border: 2px solid #e0e0e0;
        font-size: 1.1em;
        line-height: 1.5em;
        box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
    }
</style> -->