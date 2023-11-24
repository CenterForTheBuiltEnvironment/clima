function click_tab(name) {
  cy.get('.custom-tab')
    .not('.tab--disabled')
    .contains(name)
    .click();
}

describe('template spec', () => {
  it('Loads all tabs for uploaded EPW', () => {
    cy.visit('http://127.0.0.1:8080');
    cy.contains('CBE Clima Tool');
    cy.contains('Current Location: N/A');
    
    // Upload
    cy.get('input[type=file]').selectFile('test.epw', {force: true});
    cy.contains('The EPW was successfully loaded!');
    cy.contains('Current Location: Bologna Marconi AP, ITA');

    // Climate Summary
    click_tab('Climate Summary');
    cy.contains('data collected between 2004 and 2018');
    cy.contains('Longitude: 11.2969');
    cy.contains('Latitude: 44.5308');
    cy.contains('Elevation above sea level: 37.0 m');
    cy.contains('This file is based on data collected between 2004 and 2018');
    cy.contains('Köppen–Geiger climate zone: Cfa. Humid subtropical, no dry season.');
    cy.contains('Average yearly temperature: 14.5 °C');
    cy.contains('Hottest yearly temperature (99%): 34.0 °C');
    cy.contains('Coldest yearly temperature (1%): -2.0 °C');
    cy.contains('Annual cumulative horizontal solar radiation: 1546.12 kWh/m2');
    cy.contains('Percentage of diffuse horizontal solar radiation: 39.4 %');

    // Temperature and Humidity
    click_tab('Temperature and Humidity');
    cy.contains('Yearly chart');
    cy.contains('Dry bulb temperature (°C)');
    // TODO: simulate mouseover
    cy.contains('Daily chart');
    // TODO: simulate mouseover
    cy.contains('Heatmap chart');
    // TODO: simulate mouseover
    cy.contains('Descriptive statistics');
    cy.contains('12.1'); // January max

    // Sun and Clouds
    click_tab('Sun and Clouds');
    cy.contains('Sun path chart');
    // TODO
    cy.contains('Global and Diffuse Horizontal Solar Radiation (Wh/m²)');
    // TODO
    cy.contains('Cloud coverage');
    // TODO
    cy.contains('Daily charts');
    // TODO

    // Wind
    click_tab('Wind');
    cy.contains('Annual Wind Rose');
    // TODO
    cy.contains('Seasonal Wind Rose');
    cy.contains('Observations between the months of Dec and Feb between 01:00 hours and 24:00 hours.');
    cy.contains('Selected observations 2160 of 8760, or 24 %.');
    cy.contains('40 observations have calm winds.');
    // TODO
    cy.contains('Daily Wind Rose');
    // TODO
    cy.contains('Customizable Wind Rose');

    // Psychrometric Chart
    click_tab('Psychrometric Chart');

    // Natural Ventilation
    click_tab('Natural Ventilation');

    // Outdoor Comfort
    click_tab('Outdoor Comfort');

    // Data Explorer
    click_tab('Data Explorer');
  })
})