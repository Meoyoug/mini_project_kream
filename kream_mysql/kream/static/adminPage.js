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
      .then(response => response.json())
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

function update_product(){
  fetch('/update',{
    method : 'GET'
  })
  .then(response => response.json())
  .then(data => {
    if (!data.success){
      alert('업데이트 중 오류 발생')
    }
  })
}


