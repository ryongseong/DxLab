<script>
    import Image_A from "/public/image5.png?enhanced";
    import Image_Human from "/public/image3.png?enhanced";
    import { link } from "svelte-spa-router";
</script>

<style>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px;
        margin-top: 50px;
        gap: 40px;
    }

    .card-title {
        width: 481px;
        height: 113px;
        top: 131px;
        left: 140px;
        gap: 0px;
        opacity: 0px;
    }

    .card {
        /* width: 1180px;
        height: 702px;
        top: 232px;
        left: 140px; */
        gap: 0px;
        border-radius: 20px 0px 0px 0px;
        opacity: 0px;
    }

    span {
        font-family: Inter;
        font-size: 32px;
        font-weight: 400;
        line-height: 38.73px;
        text-align: left;
    }

    img.body {
        width: 334px;
        height: 284px;
        top: 266px;
        left: 185px;
        gap: 0px;
        border-radius: 174.5px 0px 0px 0px;
        opacity: 0px;
    }
    
    img.head {
        width: 101px;
        height: 101px;
        top: 131px;
        left: 140px;
        gap: 0px;
        opacity: 0px;
    }
    
    .button {
        margin-top: 10px;
        font-size: 40px;
        color: white;
        background-color: #9470F7B0;
        text-align: center;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        width: 321px;
        height: 69px;
        transition: background-color 0.3s;
    }

    .button:hover {
        background-color: #a07bfa;
    }
</style>


<div class="container">
    <div class="card-box">
        <div class="card-title">
            <img class="head" src={Image_A} alt="A+사진"/>
            <span style="text-align: center;">자격증 <strong>문제 풀기</strong></span>
        </div>
        <div class="card">
            <img class="body" src={Image_Human} alt="사람 사진"/>
            <a use:link href="/exam/detail">
                <button class="button">문제풀기</button>
            </a>
        </div>
    </div>
</div>