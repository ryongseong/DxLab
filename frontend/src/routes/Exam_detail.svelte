<script>
    import fastapi from "../lib/api";
    import Image_A from "/public/image5.png?enhanced";
    import { onMount } from "svelte";
    
    export let params;
    let examData = { title: "", questions: [] };
    let isLoading = true;
    let showAnswers = false;
    let selectedAnswers = [];
    let exam_id;
    let score = 0;

    onMount(() => {
        if (params && params.exam_id) {
            exam_id = params.exam_id;
            fetchExamData();
        } else {
            console.error("exam_id가 존재하지 않습니다.");
            isLoading = false; // Stop loading spinner if no exam_id
        }
    });

    function fetchExamData() {
        try {
            const url = `/api/exam/${exam_id}/questions`;  // 쿼리 스트링을 빼고 URL을 설정
            fastapi('get', url, null, 
                (json) => {
                    examData = json;  // 데이터가 있으면 examData에 할당
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
        const existingAnswer = selectedAnswers.find(answer => answer.question_id === questionId);
        
        if (existingAnswer) {
            existingAnswer.selected_choice_id = optionId;
        } else {
            selectedAnswers.push({ question_id: questionId, selected_choice_id: optionId });
        }
        console.log(selectedAnswers);
    }

    async function submitExam() {
        if (!exam_id) {
            console.error("exam_id 파라미터가 없습니다.");
            return;
        }

        try {
            fastapi('post', `/api/exam/${exam_id}/attempt`, {
                exam_id: exam_id,
                answers: selectedAnswers
            },
            (json) => {
                // 성공적으로 응답을 받으면 점수를 업데이트
                score = json.score;
                if (score !== undefined) {
                    showAnswers = true;
                    alert(`${score}개 맞추셨습니다.`);
                } else {
                    console.error('Invalid response:', json);
                }
            },
            (error) => {
                console.error("Error submitting exam:", error);
                alert('시험 제출 중 오류가 발생했습니다.');
            });
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
                {#each examData.questions as question, index}
                <div class="question">
                    <div class="question-title">
                        <span class="question-id">{index + 1}.</span>
                        <span class="question-text">{question.content}</span>
                    </div>
                    <ul class="options">
                        {#if showAnswers}
                            <p class="answer">
                                답: {question.choices.find(option => option.is_correct)?.content || "답 없음"}
                            </p>
                        {/if}
                        {#each question.choices as option}
                            <li
                                class="option"
                                style="color: {
                                    showAnswers && 
                                    selectedAnswers.find(answer => answer.question_id === question.id)?.selected_choice_id === option.id
                                    ? (option.is_correct ? 'blue' : 'red') 
                                    : 'inherit'
                                };"
                            >
                                <label>
                                    <input
                                        type="radio"
                                        name="question-{question.id}"
                                        checked={selectedAnswers.find(answer => answer.question_id === question.id)?.selected_choice_id === option.id}
                                        on:change={() => selectAnswer(question.id, option.id)}
                                        disabled={showAnswers}
                                    />
                                    {option.content}
                                </label>
                            </li>
                        {/each}
                    </ul>
                    {#if showAnswers && selectedAnswers.find(answer => answer.question_id === question.id)?.selected_choice_id !== question.choices.find(option => option.is_correct)?.id}
                        <p class="description">설명: {question.description}</p>
                    {/if}
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

    input[type="radio"] {
        width: 18px;
        height: 18px;
    }
</style>
