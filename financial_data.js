async function fetchData() {
    const url = 'http://0.0.0.0/api/data'
    try {
        const response = await fetch(url);
    
        if (!response.ok) {
          console.error('Error fetching data:', response.statusText);
          return;
        }

        const data = await response.json();
        console.log('Data fetched:', data);  // For demonstration only
        updateUI(data)
    } catch (error) {
      console.error('Error:', error);
    }
}

function updateUI(data) {
    const data_table = document.getElementsByClassName('data-list')[0];
    const li_headings = ['Total Liabilities', 'Total Current Liabilities', 'Total Assets',
      'Total Current Assets', 'Net Assets', 'Net Worth', 'Working Capital', 'Capital Employed',
      'Debt Ratio', 'Debt Ratio (Short-Term)', 'Debt To Equity Ratio'];
    let c = 0;
    data[0].forEach(element => {
      if (c != 11){

        let list_item = document.createElement('li');
        let list_item_label = document.createElement('h2');
        let list_item_data = document.createElement('p');
        // let chart_item = document.createElement('canvas');
        
        list_item.appendChild(list_item_label);
        list_item.appendChild(list_item_data);
        data_table.appendChild(list_item);
        list_item_label.innerHTML = `${li_headings[c]}`;
        list_item_data.innerHTML = `${element}`;
        
        // generates graphs based on each item
        generate_chart(data[0], element, c);
      }
      c += 1;
    });
}

function generate_chart(data, element, c) {
    const charts_list = document.getElementsByClassName('charts-graphs')[0];
    let list_item = document.createElement('li');
    let chart_heading = document.createElement('h2');
    let chart_item = document.createElement('canvas');

    switch (c) {
      case 1:
        charts_list.appendChild(list_item);
        list_item.appendChild(chart_heading)
        chart_heading.innerHTML = 'Liabilities';
        list_item.appendChild(chart_item);
        const liabilities_chart = new Chart(chart_item, {
            type:'pie',
            data:{
              labels:['Liabilities (Short-Term)', 'Liabilities (Long-Term)'],
              datasets:[{
                label:'test data',
                data:[element, data[c-1]-element],
                backgroundColor:['#000000', '#FF0000']
              }]
            }
          }
        );
        break;
      case 3:
          charts_list.appendChild(list_item);
          list_item.appendChild(chart_heading)
          chart_heading.innerHTML = 'Assets';
          list_item.appendChild(chart_item);
          const assets_chart = new Chart(chart_item, {
              type:'pie',
              data:{
                labels:['Assets (Liquid)', 'Assets (Non-Liquid)'],
                datasets:[{
                  label:'Assets',
                  data:[element, data[c-1]-element],
                  backgroundColor:['#000000', '#FF0000']
                }]
              }
            }
          );
          break;
      case 8:
          charts_list.appendChild(list_item);
          list_item.appendChild(chart_heading)
          chart_heading.innerHTML = 'Debt Ratio';
          list_item.appendChild(chart_item);
          const debt_ratio_chart = new Chart(chart_item, {
            type:'pie',
            data:{
              labels:['Assets', 'Liabilities'],
              datasets:[{
                label:'Debt Ratio',
                data:[1 - element, element],
                backgroundColor:['#000000', '#FF0000']
              }]
            }
          }
        );
        break;
      case 9:
        charts_list.appendChild(list_item);
        list_item.appendChild(chart_heading)
        chart_heading.innerHTML = 'Debt Ratio';
        list_item.appendChild(chart_item);
        const debt_ratio_st_chart = new Chart(chart_item, {
          type:'pie',
          data:{
            labels:['Assets (Liquid)', 'Liabilities (Short-Term)'],
            datasets:[{
              label:'Debt Ratio',
              data:[1 - element, element],
              backgroundColor:['#000000', '#FF0000']
            }]
          }
        }
      );
      break;
      case 10:
        charts_list.appendChild(list_item);
        list_item.appendChild(chart_heading)
        chart_heading.innerHTML = 'Debt To Equity Ratio';
        list_item.appendChild(chart_item);
        const debt_equity_chart = new Chart(chart_item, {
          type:'pie',
          data:{
            labels:['Shareholder Equity (Net Worth)', 'Liabilities'],
            datasets:[{
              label:'Debt To Equity Ratio',
              data:[1 - element, element],
              backgroundColor:['#000000', '#FF0000']
            }]
          }
        }
      );
      break;
      default:
        break;
    }
}

fetchData();