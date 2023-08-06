// Event handler for choice blocks with conditional visibility
function choiceHandler(target) {
  const choiceHandler = target.closest('.wagtailuiplus__choice-handler');
  if (choiceHandler !== null) {
    const choiceHandlerValue = choiceHandler.querySelector('select').value;
    const structBlockFields = choiceHandler.closest('ul.fields');
    const choiceHandlerIdRegex = /wagtailuiplus__choice-handler--([a-zA-Z\-\_]+)/;
    const choiceHandlerId = choiceHandlerIdRegex.exec(choiceHandler.className)[1];
    const choiceHandlerTargets = structBlockFields.querySelectorAll('.wagtailuiplus__choice-handler-target--' + choiceHandlerId);
    const hiddenIfRegex = /wagtailuiplus__choice-handler-hidden-if--([a-zA-Z\-\_]+)/g;
    let hiddenIfValue;
    let matches;
    let hiddenIfs;
    let hiddenIfIndex;
    for (let j = 0; j < choiceHandlerTargets.length; j++) {
      matches = hiddenIfRegex.exec(choiceHandlerTargets[j].className);
      while (matches !== null) {
        hiddenIfValue = matches[1];
        choiceHandlerTargetContainer = choiceHandlerTargets[j].closest('li');
        if (choiceHandlerValue === hiddenIfValue) {
          if (choiceHandlerTargetContainer.hasAttribute('data-wagtailuiplus-hidden-ifs')) {
            hiddenIfs = choiceHandlerTargetContainer.getAttribute('data-wagtailuiplus-hidden-ifs').split(',');
            hiddenIfs.push(hiddenIfValue);
            choiceHandlerTargetContainer.setAttribute('data-wagtailuiplus-hidden-ifs', hiddenIfs.join(','));
          } else {
            choiceHandlerTargetContainer.setAttribute('data-wagtailuiplus-hidden-ifs', hiddenIfValue);
          }
          if (!choiceHandlerTargetContainer.classList.contains('wagtailuiplus__choice-handler-target--hidden')) {
            choiceHandlerTargetContainer.classList.add('wagtailuiplus__choice-handler-target--hidden');
          }
        } else if (choiceHandlerTargetContainer.hasAttribute('data-wagtailuiplus-hidden-ifs')) {
          hiddenIfs = choiceHandlerTargetContainer.getAttribute('data-wagtailuiplus-hidden-ifs').split(',');
          hiddenIfIndex = hiddenIfs.indexOf(hiddenIfValue);
          if (hiddenIfIndex > -1) {
            hiddenIfs.splice(hiddenIfIndex, 1);
            if (hiddenIfs.length === 0) {
              choiceHandlerTargetContainer.classList.remove('wagtailuiplus__choice-handler-target--hidden');
              choiceHandlerTargetContainer.removeAttribute('data-wagtailuiplus-hidden-ifs');
            } else {
              choiceHandlerTargetContainer.setAttribute('data-wagtailuiplus-hidden-ifs', hiddenIfs.join(','));
            }
          }
        }
        matches = hiddenIfRegex.exec(choiceHandlerTargets[j].className);
      }
    }
  }
}

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

  // Bind the choice block event handler to all stream fields, so it applies to all existing and future choice blocks
  const structBlockContainers = document.querySelectorAll('.sequence-container.sequence-type-stream > .sequence-container-inner > .sequence');
  let i;
  for (i = 0; i < structBlockContainers.length; i++) {
    structBlockContainers[i].addEventListener('change', function(event) {
      choiceHandler(event.target);
    });
  }

  // Trigger the choice block event handler for all existing choice blocks
  const choiceHandlerSelects = document.querySelectorAll('.sequence-container.sequence-type-stream > .sequence-container-inner > .sequence .wagtailuiplus__choice-handler select');
  for (i = 0; i < choiceHandlerSelects.length; i++) {
    choiceHandler(choiceHandlerSelects[i]);
  }
});
