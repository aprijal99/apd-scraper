import scrapy, re

class ApdScraper(scrapy.Spider):
  name = 'ApdScraper'
  pattern = re.compile('<.*?>')

  def start_requests(self):
    apdIdList = self.getApdIdList()
    for apdId in apdIdList:
      yield scrapy.Request(
        url='https://aps.unmc.edu/database/peptide', 
        callback=self.parse, 
        method='POST',
        headers={
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body=f'ID={apdId}'
      )

  def parse(self, response):
    rows = response.xpath('//table[@class="peptide"]//tr')
    # print(rows[0].xpath('.//td')[1].xpath('.//text()').get().strip()[2:])
    # print(rows[1].xpath('.//td')[1].xpath('.//text()').get().strip())
    # print(re.sub(self.pattern, '', rows[2].xpath('.//td')[1].get()).strip())
    # print(response.xpath('//p[@class="peptide_sequence"]//text()').get())
    # print(rows[9].xpath('.//td')[1].xpath('.//text()').get().strip())

    yield {
      'APD ID': str(rows[0].xpath('.//td')[1].xpath('.//text()').get().strip()[2:]),
      'Name': rows[1].xpath('.//td')[1].xpath('.//text()').get().strip(),
      'Sequence': response.xpath('//p[@class="peptide_sequence"]//text()').get(),
      'Source': re.sub(self.pattern, '', rows[2].xpath('.//td')[1].get()).strip()
    }

  def getApdIdList(self):
    apdIdList = []
    with open('APD_sequence_release_09142020.fasta', 'r') as f:
        for line in f.readlines():
          if('plants' in line):
            apdIdList.append(line[1:6])

    return apdIdList