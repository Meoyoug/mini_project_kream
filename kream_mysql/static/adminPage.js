function updateDate(){
    const header = document.getElementById('db-header')
    let current = new Date();
    let nextTime = new Date();
    nextTime.setHours(nextTime.getHours() + 1);
    nextTime.setMinutes(0);
    nextTime.setSeconds(0);
    let timeInterval = nextTime - current

    header.textContent = `신규 등록 상품 (${current.getFullYear()}-${('0' + current.getMonth()+1).slice(-2)}-${('0' + current.getDate()).slice(-2)} ${('0' + current.getHours()).slice(-2)}시)`
    setTimeout(updateDate,timeInterval);
}
function delete_product(){
    var checked_checkbox = document.querySelectorAll('input.category_checkbox:checked');
    var selected_rows=[];
    checked_checkbox.forEach(function(checkbox){
      var row = checkbox.closest('tr');
      var product = row.querySelector('td:nth-child(4)').textContent;
      console.log(product)
      selected_rows.push(product)
    })
    console.log(selected_rows)

    if(selected_rows.length > 0){
      fetch('/delete_data',{
        method : 'post',
        headers: {
          'Content-Type' : 'application/json',
        },
        body: JSON.stringify({products : selected_rows})
      })
      .then(response => response)
      .then(data => {
        if (data.success){
          checked_checkbox.forEach(function(checkbox){
            checkbox.closest('tr').remove();
          });
        } else {
          alert('삭제 중 오류 발생')
        }
      });
    } else {
      alert('삭제할 항목을 선택하고 버튼을 눌러주세요.')
    }
}

const search_form = document.getElementById('search_form')

search_form.addEventListener('submit', function(event){
  event.preventDefault();
  const formdata = new FormData(search_form);
  const search_data = {
    category : [],
    gender : [],
  }
  // 폼으로 입력받은 검색 조건을 search_data라는 객체에 저장
  for (const pair of formdata.entries()) {
    if(pair[0] == 'category'){
      search_data['category'].push(pair[1]);
    } 
    else if (pair[0] == 'gender'){
      if (pair[1] == '남성'){
        search_data['gender'].push('male');
      }
      else if (pair[1] == '여성'){
        search_data['gender'].push('female');
      }
      else if (pair[1] == '남여공용'){
        search_data['gender'].push('unisex');
      }
      else if (pair[1] == '키즈'){
        search_data['gender'].push('kids');
      }
    }
    else if (pair[0] == 'search_word') {
      search_data['search_word'] = pair[1];
    }
  }
  // 만약 검색어가 있으면 post 요청으로 검색데이터를 전달
  if(search_data['search_word'] || search_data['category'] || search_data['gender']){
    fetch('/search_data', {
      method: 'post',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ search_data: search_data })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success){
        const dataTable = document.getElementById('data-table');
    
        // 데이터를 받아온 경우, 기존 테이블 내용을 지우고 새로운 데이터로 채우기
        dataTable.innerHTML = ''; 

        // 받은 데이터를 반복하여 테이블에 추가
        data.current_datas.forEach(dataItem => {
            const row = document.createElement('tr');

        // 각 열에 데이터 추가
        row.innerHTML = `
            <td>&nbsp;&nbsp;<input type="checkbox" class="category_checkbox"></td>
            <td>${dataItem[0]}</td>
            <td>${dataItem[1]}</td>
            <td>${dataItem[2]}</td>
            <td>${dataItem[3]} 원</td>
            <td>${dataItem[4] !== null ? dataItem[4] : 'N/A'}</td>
        `;

        // 테이블에 행 추가
        dataTable.appendChild(row);
        });
      }
      else {
        location.reload()
      }
    })
  }
})
  //페이지가 로드되면 실행될 함수
window.onload = function(){
    updateDate();
}

