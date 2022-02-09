const SmileyTable = {
  1: 'Angry_Emoji.png',
  2: 'sad.png',
  3: 'confused.png',
  4: 'smiling.png',
  5: 'outstanding.png',
}

function getSmileyImgPath (val) {
  return `/static/img/emojis/${SmileyTable[val]}`
}

export default getSmileyImgPath
