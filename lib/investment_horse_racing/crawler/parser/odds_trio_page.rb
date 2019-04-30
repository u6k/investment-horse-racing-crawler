require "nokogiri"
require "crawline"

module InvestmentHorseRacing::Crawler::Parser
  class OddsTrioPageParser < Crawline::BaseParser
    def initialize(url, data)
      @logger = InvestmentHorseRacing::Crawler::AppLogger.get_logger
      @logger.debug("OddsTrioPageParser#initialize: start: url=#{url}, data.size=#{data.size}")

      @data = data

      _parse(url, data)
    end

    def redownload?
      @logger.debug("OddsTrioPageParser#redownload?: start")

      return false if (Time.now.utc - @data["downloaded_timestamp"]) < (24 * 60 * 60)

      start_date = Time.local(@start_datetime.year, @start_datetime.month, @start_datetime.day)

      (Time.now - start_date) < (90 * 24 * 60 * 60)
    end

    def valid?
      (@title === "3連複")
    end

    def related_links
      @related_links
    end

    def parse(context)
      # TODO: Parse all result info
      context["odds_trio"] = {
        @odds_trio_id => {}
      }
    end

    private

    def _parse(url, data)
      @logger.debug("OddsTrioPageParser#_parse: start")

      @odds_trio_id = url.match(/^.+?\/odds\/sf\/([0-9]+)\/$/)[1]
      @logger.debug("OddsTrioPageParser#_parse: @odds_trio_id=#{@odds_trio_id}")

      doc = Nokogiri::HTML.parse(data["response_body"], nil, "UTF-8")

      doc.xpath("//li[@id='raceNavi2C']").each do |li|
        @logger.debug("OddsTrioPageParser#_parse: li=#{li.inspect}")

        @title = li.children[0].text.strip
        @logger.debug("OddsTrioPageParser#_parse: @title=#{@title}")
      end

      doc.xpath("//p[@id='raceTitDay']").each do |p|
        @logger.debug("OddsTrioPageParser#_parse: p=#{p.inspect}")

        date = p.children[0].text.strip.match(/^([0-9]+)年([0-9]+)月([0-9]+)日/) do |date_parts|
          Time.new(date_parts[1].to_i, date_parts[2].to_i, date_parts[3].to_i)
        end

        time = p.children[4].text.strip.match(/^([0-9]+):([0-9]+)発走/) do |time_parts|
          Time.new(1900, 1, 1, time_parts[1].to_i, time_parts[2].to_i, 0)
        end

        if (not date.nil?) && (not time.nil?)
          @start_datetime = Time.new(date.year, date.month, date.day, time.hour, time.min, 0)
          @logger.debug("OddsTrioPageParser#_parse: @start_datetime=#{@start_datetime}")
        end
      end

      @related_links = doc.xpath("//div[@id='raceNavi2']/ul/li").map do |li|
        if not li.children[0]["href"].nil?
          li.children[0]["href"].match(/^(\/odds\/.+?\/[0-9]+\/).*$/) do |path|
            @logger.debug("OddsTrioPageParser#_parse: path=#{path.inspect}")
            URI.join(url, path[1]).to_s
          end
        end
      end

      @related_links.compact!

      @related_links.each do |related_link|
        @logger.debug("OddsTrioPageParser#_parse: related_link=#{related_link}")
      end
    end
  end
end
