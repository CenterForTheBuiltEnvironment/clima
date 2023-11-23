describe('template spec', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8080');
    cy.contains('CBE Clima Tool');
    cy.contains('Current Location: N/A');
  })
})