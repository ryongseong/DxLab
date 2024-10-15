<script>
  import Router from 'svelte-spa-router'
  import GPT from "./routes/GPT.svelte"
  import UserCreate from './routes/UserCreate.svelte';
  import UserLogin from './routes/UserLogin.svelte';
  import Navigation from './components/Header.svelte';
  import QuestionModify from './routes/QuestionModify.svelte';
  import Home from './routes/Home.svelte';
  import Exam from './routes/Exam.svelte';
  import ExamDetail from './routes/Exam_detail.svelte';
  import { wrap } from 'svelte-spa-router/wrap'; 
  import Gemini from './routes/GEMINI.svelte';
  import SelectSelf from './routes/Select_self.svelte';

  const routes = {
    '/': Home,
    '/select': SelectSelf,
    '/self': GPT,
    '/self-gen': Gemini,
    '/exam': Exam,
    '/exam-detail/:exam_id': ExamDetail,
    '/question-modify/:question_id': QuestionModify,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
  }
</script>

<Navigation />
<Router {routes}/>