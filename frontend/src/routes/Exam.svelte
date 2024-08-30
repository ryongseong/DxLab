<script>
    import Image_A from "/public/image5.png?enhanced";
    import Image_Human from "/public/image3.png?enhanced";
    import { link } from "svelte-spa-router";

    let certifications = [
        "정보처리산업기사",
        "정보처리기사",
        "정보기기운용기능사",
        "워드프로세스",
        "항공기사",
        "전자기기기능사",
        "전자산업기사",
        "토목기능사",
        "축산산업기사",
        "소음진동기사"
    ];

    let selectedCertification = '';

    function toggleSelection(certification) {
        if (selectedCertification === certification) {
            selectedCertification = '';
        } else {
            selectedCertification = certification;
        }
    }
</script>

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
        width: 342px;
    }

    .certification-item input {
        margin-right: 10px;
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

    .speech-bubble::before {
        content: '   ';
        position: absolute;
        bottom: -20px;
        left: 20px;
        width: 0;
        height: 0;
        border-left: 20px solid transparent;
        border-right: 20px solid transparent;
        border-top: 20px solid white;
    }
</style>

<div class="container">
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
                {#each certifications as certification}
                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <!-- svelte-ignore a11y-no-static-element-interactions -->
                    <div 
                        class="certification-item"
                        on:click={() => toggleSelection(certification)}
                    >
                        <input
                            type="checkbox"
                            checked={selectedCertification === certification}
                            on:change={() => toggleSelection(certification)}
                        />
                        {certification}
                    </div>
                {/each}
            </div>
        </div>
        <a use:link href="/exam/detail">
            <button class="button">문제풀기</button>
        </a>
    </div>
</div>
