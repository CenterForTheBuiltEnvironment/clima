describe('template spec', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8080');
    cy.contains('CBE Clima Tool');
    cy.contains('Current Location: N/A');
    
    // Upload
    cy.get('input[type=file]').selectFile('test.epw', {force: true});
    cy.contains('The EPW was successfully loaded!');

    cy.get('.custom-tab').not('.tab--disabled').contains('Climate Summary', {timeout: 30 * 1000}).click();
    cy.contains('data collected between 2004 and 2018')
  })
})