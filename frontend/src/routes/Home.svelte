<!--  fastapi 함수를 사용할수 있게 import문을 추가했다. 
질문 목록 API는 GET방식이므로 operation 항목에 'get'을 전달했고, 
추가로 전달할 파라미터 값은 아직 없기 때문에 params 항목은 빈 값인 {}을 전달했다. 
그리고 success_callback 함수는 다음과 같이 화살표 함수로 작성하여 전달했다-->
<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import {page, keyword, is_login} from "../lib/store"
    import moment from "moment/min/moment-with-locales"
    moment.locale('ko')  // 한국식 시간 표시


    let question_list = []
    // 페이지 리스트 추가
    let size = 10
    //let page = 0 - store.js page 를 사용
    let kw = ''  // 검색어
    let total =0
    $: total_page = Math.ceil(total/size)

    function get_question_list() {
        let params = {
            page: $page,
            size: size,
            keyword: $keyword,
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            total = json.total
            kw = $keyword
        })
    }

    $:$page, $keyword, get_question_list()
    // $: 의 의미는 page 값이 변경될 경우 get_question_list 함수도 다시 호출하는 것
</script>

<!--웹 디자인, 부트스트립 적용-->
<div class="container my-3">
    <div class="row my-3">
      <div class="col-6">
          <a use:link href="/question-create" 
              class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
      </div>
      <div class="col-6">
          <div class="input-group">
              <input type="text" class="form-control" bind:value="{kw}">
              <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}} >
                  찾기
              </button>
          </div>
      </div>
  </div>
  <table class="table">
      <thead>
      <tr class="text-center table-dark">
          <th>번호</th>
          <th style="width:50%">제목</th>
          <th>글쓴이</th>
          <th>작성일시</th>
      </tr>
      </thead>
      <tbody>
      {#each question_list as question, i}
      <tr class="text-center">
          <td>{total - ($page * size) - i}</td>  <!--게시물 번호 공식 적용-->
          <td class="text-start">
              <a use:link href="/detail/{question.id}">{question.subject}</a>
              <!--질문에 달린 답변 개수 표시-->
              {#if question.answers.length > 0}
              <span class = "text-danger small mx-2">{question.answers.length}</span>
              {/if}
          </td>
          <td>{ question.user ? question.user.username : "" }</td>
          <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
      </tr>
      {/each}
      </tbody>
  </table>
  <!--페이지 처리 시작 -->
  <ul class="pagination justify-content-center">
    <!--이전페이지-->
    <li class="page-item {page <= 0 && 'disabled'}">
      <button class="page-link" on:click ="{()=> $page--}">이전</button>
    </li>
    <!--페이지번호-->
    {#each Array(total_page) as _, loop_page}
    {#if loop_page >= $page-5 && loop_page <= $page+5}
    <li class="page-item {loop_page === $page && 'active'}">
      <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
    </li>
    {/if}
    {/each}
    <!-- 다음페이지 -->
    <li class="page-item {$page >= total_page-1 && 'disabled'}">
        <button class="page-link" on:click="{() => $page++}">다음</button>
    </li>
  </ul>
  <!-- 페이징처리 끝 -->

</div>

