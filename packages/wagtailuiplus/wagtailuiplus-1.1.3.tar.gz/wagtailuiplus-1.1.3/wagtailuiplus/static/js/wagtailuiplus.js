function updateStructBlockHeader(event) {
  const field = event.target.closest('li');
  if (event.target.tagName !== 'INPUT' || field === null || field.previousElementSibling !== null) {
    return;
  }
  const headerLabel = field.closest('.sequence-member').querySelector('.sequence-controls > h3 > label');
  if (headerLabel === null) {
    return;
  }
  if (!headerLabel.hasAttribute('data-original-text')) {
    headerLabel.dataset.originalText = headerLabel.innerText;
  }
  headerLabel.innerText = headerLabel.dataset.originalText + ' - ' + event.target.value;
}

document.addEventListener('DOMContentLoaded', function() {

  // Make the panels collapsable
  let i;
  const panelHeaders = document.querySelectorAll('.object > h2');
  for (i = 0; i < panelHeaders.length; i++) {
    panelHeaders[i].addEventListener('click', function() {
      if (this.parentElement.classList.contains('wagtailuiplus__panel--collapsed')) {
        this.parentElement.classList.remove('wagtailuiplus__panel--collapsed');
      } else {
        this.parentElement.classList.add('wagtailuiplus__panel--collapsed');
      }
    });
  }

  let sequenceControls;
  const structBlockContainers = document.querySelectorAll('.sequence-container.sequence-type-stream > .sequence-container-inner > .sequence');
  for (i = 0; i < structBlockContainers.length; i++) {
    // Make the struct block headers collapsable
    structBlockContainers[i].addEventListener('click', function(event) {
      sequenceControls = event.target.closest('.sequence-controls');
      if (sequenceControls === null) {
        return;
      }
      if (this.id !== event.target.closest('.sequence').id) {
        return;
      }

      if (sequenceControls.parentElement.classList.contains('wagtailuiplus__struct-block--collapsed')) {
        sequenceControls.parentElement.classList.remove('wagtailuiplus__struct-block--collapsed');
      } else {
        sequenceControls.parentElement.classList.add('wagtailuiplus__struct-block--collapsed');
      }
    });

    // Make the first field of a struct block update the header text
    structBlockContainers[i].addEventListener('change', function(event) {
      updateStructBlockHeader(event);
    });
    structBlockContainers[i].addEventListener('keyup', function(event) {
      updateStructBlockHeader(event);
    });
  }

  // Set the initial collapsed state of existing struct blocks
  let fields;
  let headerLabel;
  const structBlocks = document.querySelectorAll('.sequence-container.sequence-type-stream > .sequence-container-inner > .sequence > .sequence-member');
  for (i = 0; i < structBlocks.length; i++) {
    // structBlocks[i].classList.add('wagtailuiplus__struct-block--collapsed');
    fields = structBlocks[i].querySelectorAll('.field');
    if (fields.length === 0) {
      continue;
    }
    headerLabel = structBlocks[i].querySelector('.sequence-controls > h3 > label');
    headerLabel.dataset.originalText = headerLabel.innerText;
    if (fields[0].classList.contains('char_field')) {
      structBlocks[i].classList.add('wagtailuiplus__struct-block--collapsed'); // remove this when uncommenting the line above
      headerLabel.innerText = headerLabel.dataset.originalText + ' - ' + fields[0].querySelector('input[type=text]').value;
    } else if (fields[0].classList.contains('model_choice_field')) {
      // uncomment this to enable model choice field based headers, todo: update header on change of model choice
      // headerLabel.innerText = headerLabel.dataset.originalText + ' - ' + fields[0].querySelector('.chosen .title').innerText;
    }
  }
});
