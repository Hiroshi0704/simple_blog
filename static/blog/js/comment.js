  var commentList = document.querySelectorAll('#commentList li');
  var moreBtn = document.querySelector('#moreBtn');
  var closeBtn = document.querySelector('#closeBtn');
  console.log(commentList);
  
  var commentLength = commentList.length;
  var defaultNum = 3;
  var addNum = 3;
  var currentNum = 0;

  function initView() {
    closeBtn.style.display = 'none';
    currentNum = defaultNum;
    if (currentNum < commentLength) {
      moreBtn.style.display = 'block';
    } else {
      moreBtn.style.display = 'none';
    }

    showComment();
  }

  function showComment() {
    for (i=0; i < commentLength; i++) {
      if (i < currentNum) {
        commentList[i].style.display = 'block';
      } else {
        commentList[i].style.display = 'none';
      }
    }
  }

  function showMore() {
    currentNum += addNum;
    showComment();
    checkMoreData();
  }

  function closeData() {
    initView();
  }

  function checkMoreData() {
    if (currentNum >= commentLength) {
      moreBtn.style.display = 'none';
      closeBtn.style.display = 'block';
    }
  }
  moreBtn.addEventListener('click', showMore);
  closeBtn.addEventListener('click', closeData);
  initView();