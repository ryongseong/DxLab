<script>
    import Image_A from "/public/image5.png?enhanced";
    import Image_Human from "/public/image3.png?enhanced";
    import { link, push } from "svelte-spa-router";
    import { onMount } from "svelte";
    import fastapi from "../lib/api";
    import { fetchCertifications } from "../lib/auth";
    import { certifications } from "../lib/store";

    let isLoading = true;

    let selectedCertification = 0;

    function toggleSelection(certification) {
        if (selectedCertification === certification.exam_id) {
            selectedCertification = 0;
        } else {
            selectedCertification = certification.exam_id;
        }
    }

    function handleExamDetail(selectedCertification) {
        if (selectedCertification === '') {
            alert('자격증을 선택해주세요!');
        } else {
            push(`/exam-detail/${selectedCertification}`);
        }
    }

    
    onMount(async () => {
        try {
            await fetchCertifications();
            console.log($certifications);
        } catch (error) {
            console.error('Error fetching exam data:', error);
        } finally {
            isLoading = false;
        }
    })
</script>

<div class="container">
    {#if isLoading}
        <p>Loading...</p>
    {:else}
        <div class="card-title">
            <img class="head" src={Image_A} alt="A+사진" />
            <p>
                자격증 <strong>문제 풀기</strong>
            </p>
        </div>
        <div class="card">
            <div style="display: flex; align-items: center;">
                <img class="body" src={Image_Human} alt="사람 사진" />
                <div class="speech-bubble">
                    원하는 자격증을 선택해 주세요!! <br />
                    <span style="color: #8a56d8; font-weight: bold;">자격증시험 선택하기</span>
                </div>
            </div>
            <div class="text-box">
                <div class="certification-list">
                    {#each $certifications as certification}
                        <!-- svelte-ignore a11y-click-events-have-key-events -->
                        <!-- svelte-ignore a11y-no-static-element-interactions -->
                        <div
                            class="certification-item"
                            on:click={() => toggleSelection(certification)}
                        >
                            <input
                                type="checkbox"
                                checked={selectedCertification === certification.exam_id}
                                on:change={() => toggleSelection(certification)}
                            />
                            {certification.title}
                        </div>
                    {/each}
                </div>
            </div>
            <button class="button" on:click={handleExamDetail(selectedCertification)}>문제풀기</button>
        </div>
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

    .card {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        background-color: #e7dbff;
        padding: 20px;
        border-radius: 15px;
        width: 100%;
        position: relative;
    }

    .body {
        width: 334px;
        height: 284px;
        margin-right: 20px;
        margin-left: 5rem;
    }

    .text-box {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 10px;
        width: 100%;
        height: 100%;
    }

    .certification-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        width: 80%;
        text-align: center;
        margin-top: 3rem;
        height: 100%;
    }

    .certification-item {
        display: flex;
        align-items: center;
        background-color: white;
        height: 3rem;
        width: 342px;
        border-radius: 7px;
        font-size: 20px;
    }

    .certification-item input {
        margin-right: 10px;
        margin-left: 1rem;
    }

    .button {
        margin-top: 20px;
        font-size: 24px;
        color: white;
        background-color: #9470f7b0;
        text-align: center;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        width: 200px;
        height: 50px;
        transition: background-color 0.3s;
        align-self: flex-end;
        margin-left: 450%;
    }

    .button:hover {
        background-color: #a07bfa;
    }

    .speech-bubble {
        position: relative;
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        font-size: 18px;
        color: #8a56d8;
        margin-bottom: 20px;
        max-width: 300px;
        text-align: center;
        margin-left: 20px;
    }

    .speech-bubble::after {
        content: '';
        position: absolute;
        top: 50%;
        left: -20px;
        border-width: 10px;
        border-style: solid;
        border-color: transparent white transparent transparent;
    }
</style>