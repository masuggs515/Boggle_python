$guessForm = $('#guess-form');
$guessText = $('#guess-text');
$newGameBtn = $('#new-game-btn');

let score = 0;
let words =[];

$newGameBtn.on('click', ()=> location.reload())

async function handleFormSubmit(e){
    e.preventDefault();
    let msg;
    let word = $guessText.val()
    
    const res = await axios.get('/check-word', {params: { word: word } });
    

    
    if(res.data.result == 'not-word'){
        msg = "Not an English word"
    } else if(res.data.result == 'not-on-board'){
        msg = "Word not found on board"
    }else{
        if(words.includes(word)){
            msg = "Words already guessed";
            $guessText.val('')
        }else{
        msg = "Congrats! Word added to score!"
        score = score + word.length
        words.push(word)
        }
    }



    wordInputRespondMessage(msg, score);
    $guessText.val('');

}

$guessForm.on('submit', handleFormSubmit);

function wordInputRespondMessage(msg, score){
    $('#word-msg').text(msg)
    $('#score').text(score)
}

let count = 60, timer = setInterval(() => {
    $('#time').html(count--);
    if(count < 0){
         clearInterval(timer);
         gameEnd();
        }
}, 1000);


async function gameEnd(){
    
    $guessForm.html('<h3>GAME OVER</h3>');
    const resp = await axios.post("/post-score", { score: score });
    if (resp.data.brokeRecord) {
        $('#score-p').text(`New record: ${score}`)
    } else {
        $('#score-p').text(`Final Score: ${score}`)
    }
    }

