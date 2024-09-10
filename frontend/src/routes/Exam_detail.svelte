<script>
    import fastapi from "../lib/api";
    import Image_A from "/public/image5.png?enhanced";
    import { onMount } from "svelte";
    
    export let params; // props로 params를 가져옴
    let examData = { title: "", questions: [] };
    let isLoading = true;
    let showAnswers = false;
    let selectedAnswers = [];
    let exam_id;

    onMount(() => {
        // params를 콘솔에 출력해서 제대로 전달되는지 확인
        console.log("Params:", params);

        // params.exam_id 값이 존재하는지 확인
        if (params && params.exam_id) {
            exam_id = params.exam_id;
        } else {
            console.error("exam_id가 존재하지 않습니다.");
            return;
        }
        
        fetchExamData()
    });

    function fetchExamData() {
        try {
            const url = `/api/exam/${exam_id}/questions`;  // 쿼리 스트링을 빼고 URL을 설정
            fastapi('get', url, null, 
                (json) => {
                    console.log("Success:", json[0]);
                    json.forEach(element => {
                        examData = element
                    });
                    // examData = json;  // 데이터가 있으면 examData에 할당
                },
                (error) => {
                    console.error("Error fetching exam data:", error);
                }
            );
        } catch (error) {
            console.error('Error fetching exam data:', error);
            examData = { title: "시험 데이터를 불러올 수 없습니다.", questions: [] };
        } finally {
            isLoading = false;
        }
    }

    function selectAnswer(questionId, optionId) {
        selectedAnswers = selectedAnswers.map(answer => 
            answer.questionId === questionId 
            ? { ...answer, selectedChoiceId: optionId } 
            : answer
        );

        if (!selectedAnswers.find(answer => answer.questionId === questionId)) {
            selectedAnswers.push({ questionId, selectedChoiceId: optionId });
        }
    }

    async function submitExam() {
        if (!exam_id) {
            console.error("exam_id 파라미터가 없습니다.");
            return;
        }
        try {
            const response = await fastapi('post', `/api/exam/${exam_id}/attempt`, {
                exam_id: examId,
                answers: selectedAnswers
            });

            if (response && response.score !== undefined) {
                showAnswers = true;
                alert(`${response.score}개 맞추셨습니다.`);
            } else {
                console.error('No valid data received:', response);
            }
        } catch (error) {
            console.error('Error submitting exam:', error);
            alert('시험 제출 중 오류가 발생했습니다.');
        }
    }
</script>

<div class="container">
    {#if isLoading}
        <p>Loading...</p>
    {:else if examData.title}
        <div class="card-title">
            <img src={Image_A} alt="A+사진" class="head">
            <h1>{examData.title}</h1>
        </div>
        <div class="card-container">
            <div class="card-box">
                {#each examData.questions as question}
                <div class="question">
                    <div class="question-title">
                        <span class="question-id">{question.id}.</span>
                        <span class="question-text">{question.content}</span>
                    </div>
                    <ul class="options">
                        {#if showAnswers}
                            <p class="answer">
                                답: {question.choices.find(option => option.is_correct).content}
                            </p>
                        {/if}
                        {#each question.choices as option}
                            <li
                                class="option"
                                style="color: {showAnswers && selectedAnswers.find(answer => answer.questionId === question.id)?.selectedChoiceId === option.id ? (option.is_correct ? 'blue' : 'red') : 'inherit'};"
                            >
                                <label>
                                    <input
                                        type="radio"
                                        name="question-{question.id}"
                                        checked={selectedAnswers.find(answer => answer.questionId === question.id)?.selectedChoiceId === option.id}
                                        on:change={() => selectAnswer(question.id, option.id)}
                                        disabled={showAnswers}
                                    />
                                    {option.content}
                                </label>
                            </li>
                        {/each}
                    </ul>
                </div>
                {/each}
            </div>
            <div class="button-wrapper">
                <button class="submit-button" on:click={submitExam} disabled={showAnswers}>결과 확인하기</button>
            </div>
        </div>
    {:else}
        <p>시험 정보를 불러오는 중 오류가 발생했습니다.</p>
    {/if}
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        border-radius: 20px;
        width: 1180px;
        height: 803px;
        margin: 0 auto;
    }

    .card-title {
        display: flex;
        align-items: flex-end;
        gap: 15px;
        font-size: 32px;
        color: #8a56d8;
        margin-bottom: 20px;
        align-self: flex-start;
    }

    .card-title img {
        width: 101px;
        height: 101px;
    }

    .card-container {
        height: 715px;
        border-radius: 20px !important;
        width: 100%;
        overflow-y: auto;
        scrollbar-width: thin; /* Firefox */
        scrollbar-color: #9470F7 white; /* Firefox */
        background-color: #AD9BF45E;
    }

    /* 웹킷 브라우저를 위한 스크롤바 스타일 */
    .card-container::-webkit-scrollbar {
        width: 10px;
    }

    .card-container::-webkit-scrollbar-thumb {
        background-color: #9470F7;
        border-radius: 10px;
    }

    .card-box {
        margin-left: 7rem;
        margin-top: 2rem;
    }

    .question-title {
        font-size: 32px;
        padding: 10px;
    }

    .question-id {
        margin-right: 1rem;
    }

    .question {
        font-size: 32px;
        margin-bottom: 20px;
    }

    .options {
        list-style-type: none;
        padding-left: 0;
        margin-top: 1rem;
        margin-left: 1rem;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    /* .option {
        margin-bottom: 5px;
    }
    
    .option input {
        margin-right: 10px;
        transform: scale(1.5);
    } */

    .answer {
        text-align: end;
        margin-right: 8rem;
    }

    .submit-button {
        padding: 10px 20px;
        background-color: #9470F7;
        color: white;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        display: block;
        text-align: right;
        margin-left: auto;
        margin-right: 2rem;
    }

    .submit-button:hover {
        background-color: #8a56d8;
    }
    .button-wrapper {
        display: flex;
        margin-bottom: 20px;
    }
</style>