# UTCI explained

The UTCI tab allows users to analyze outdoor thermal comfort for a combination of different meteorological conditions based on the presence or absence of sun and wind.&#x20;

![Logos highlighting the different scenarios which can be displayed in Clima](<../../../.gitbook/assets/UTCI 01-01.jpg>)

Clima leverages the several models implemented in [Pythermalcomfort](https://pythermalcomfort.readthedocs.io/en/latest/).

* The "[Solar gain on people](https://pythermalcomfort.readthedocs.io/en/latest/reference/pythermalcomfort.html#solar-gain-on-people)" calculates the solar gain to the human body, so the mean radiant temperature. To simulate a sunless situation, Clima considers the person surrounded by surfaces that shade him, all of which tend toward dry bulb temperature;
* Wind data is obtained directly from the weather file. The windless situation sets the value at 0.5 m/s, which is the minimum value allowed by the UTCI model.

The UTCI can then be visualized for the entire year for the scenario chosen.&#x20;

<figure><img src="../../../.gitbook/assets/Perceived T copia.png" alt=""><figcaption><p>UTCI perceived temperature annual heatmap in the four conditions for <strong>Rome, ITA</strong></p></figcaption></figure>

The values are then converted into a scale assessing thermal stress, either because of cold or heat. Therefore, a second chart maps if people will experience thermal stress for all the hours of the year for corresponding UTCI temperatures.

<figure><img src="../../../.gitbook/assets/UTCI Index copia.png" alt=""><figcaption><p>UTCI heat stress index heatmap in the four conditions for <strong>Rome, ITA</strong></p></figcaption></figure>

The UTCI is a useful tool to design the outdoor space, to maximize the number of comfortable hours. The designer can influence two factors out of the four driving outdoor comfort: radiant temperature (i.e. exposure to the sun) and wind speed (i.e. exposure to the wind).&#x20;
