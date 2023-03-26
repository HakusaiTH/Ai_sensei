const result = document.getElementById('result');
const dataInput = document.getElementById('data');
const ai_chat = document.getElementById('ai_chat');
const kanjiList = document.getElementById('kanjiList');
const wordList = document.getElementById('wordList');

const data_box = document.getElementById('data_box');
function data_box_function(sta){
  if(data_box) {
    if(sta == 'kanji'){
      document.getElementById('kanji').style.display = 'flex';
      document.getElementById('word').style.display = 'none';
    }
    else{
      document.getElementById('kanji').style.display = 'none';
      document.getElementById('word').style.display = 'flex';    
    }
    data_box.style.display = 'flex';
    console.log('pass');
  }
  else {
    console.log('data_box is null');
  }
}

document.getElementById('close').addEventListener('click',()=>{
  data_box.style.display = 'none';
})


document.getElementById('close').addEventListener('click',()=>{
  data_box.style.display = "none"
  document.getElementById('kanji').style.display = "none"
  document.getElementById('word').style.display = "none"
})


//positive negative neutral
function sen_img(param){
  if(param == 'positive'){sen_url = '/static/image/h.png'}
  else if(param == 'negative'){sen_url = '/static/image/s.png'}
  else {sen_url = '/static/image/n.png'}
  document.getElementById('sen_img').src = sen_url;
}

$('#submitBtn').click(function(event) {
  event.preventDefault();
  result.textContent = 'Transcribing...';
  $.ajax({
    type: "POST",
    url: "/generate",
    data: {
      data: dataInput.value
    },
    success: function(response) {
      ai_chat.textContent = response.ai;
      result.textContent = response.response;
      
      kanjiList.innerHTML = '';
      wordList.innerHTML = '';

      const kanji = response.kanji;
      const word = response.word;

      sen_img(response.sen);

      //kanji
      kanji.forEach(kanji => {
        const kanjiItem = document.createElement('li');
        const kanjiLink = document.createElement('a');
        kanjiLink.target = '#';
        kanjiLink.textContent = kanji;
        kanjiItem.appendChild(kanjiLink);
        kanjiList.appendChild(kanjiItem);

        kanjiLink.addEventListener('click', function(event) {
          event.preventDefault();
          $.ajax({
            type: "POST",
            url: "/dec_kanji",
            data: {
              data: kanji
            },
            success: function(response) {    
              var image_url = response.image_url
              var charater = response.charater;
              var translation_charater = response.translation_charater;
              var kun = response.kun;
              var on = response.on;
              var example = response.example;

              data_box_function('kanji');
              document.getElementById('kanji_img').src = image_url;
              document.getElementById('kanji_text').textContent = `${charater}  ${translation_charater}`;  
              document.getElementById('kun').textContent = kun;
              document.getElementById('on').textContent = on;
              document.getElementById('kanji_example').textContent = example

              console.log(image_url,charater,translation_charater,kun,on,example);
            }
          });
        });
      });

      //word
      word.forEach(word => {
        const wordItem = document.createElement('li');
        const wordLink = document.createElement('a');
        wordLink.target = '#';
        wordLink.textContent = word;
        wordItem.appendChild(wordLink);
        wordList.appendChild(wordItem);
        wordLink.addEventListener('click', function(event) {
          event.preventDefault();
          $.ajax({
            type: "POST",
            url: "/dec_word",
            data: {
              data: word
            },
            success: function(response) {
              var result = response.result;
              var translation_example = response.translation_example;
              var example = response.example;
              var word = response.word;

              data_box_function('word');
              document.getElementById('word_text').textContent = word;
              document.getElementById('word_tran').textContent = `${word}  ${result}`
              document.getElementById('word_example').textContent = example;
              document.getElementById('word_example_tran').textContent = translation_example;

              console.log(word,result,example,translation_example);
            }
          });
        });
      });
    }
  });
});