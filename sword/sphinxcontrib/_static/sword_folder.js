function toggleFold(objID)
{
  var fold;
  fold = document.getElementById(objID);
  if(fold.className == 'closed-fold')
  {
    fold.className = 'open-fold';
  }
  else if (fold.className == 'open-fold')
  {
    fold.className = 'closed-fold';
  }
}
