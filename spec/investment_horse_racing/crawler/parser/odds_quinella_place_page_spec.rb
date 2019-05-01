require "timecop"
require "webmock/rspec"

require "spec_helper"

RSpec.describe InvestmentHorseRacing::Crawler::Parser::OddsQuinellaPlacePageParser do
  before do
    WebMock.enable!

    @downloader = Crawline::Downloader.new("investment-horse-racing-crawler/#{InvestmentHorseRacing::Crawler::VERSION}")

    # 2018-06-24 hanshin 1R odds quinella place page parser
    @url = "https://keiba.yahoo.co.jp/odds/wide/1809030801/"
    WebMock.stub_request(:get, @url).to_return(
      status: [200, "OK"],
      body: File.open("spec/data/odds_quinella_place.20180624.hanshin.1.html").read)

    @parser = InvestmentHorseRacing::Crawler::Parser::OddsQuinellaPlacePageParser.new(@url, @downloader.download_with_get(@url))

    # error page parser
    @url_error = "https://keiba.yahoo.co.jp/odds/wide/0000000000/"
    WebMock.stub_request(:get, @url_error).to_return(
      status: [200, "OK"],
      body: File.open("spec/data/odds_quinella_place.00000000.error.html").read)

    @parser_error = InvestmentHorseRacing::Crawler::Parser::OddsQuinellaPlacePageParser.new(@url_error, @downloader.download_with_get(@url_error))

    WebMock.disable!
  end

  describe "#redownload?" do
    context "2018-06-24 hanshin 1R odds quinella place page" do
      it "redownload if newer than 30 days" do
        Timecop.freeze(Time.local(2018, 7, 24, 10, 4, 0)) do
          expect(@parser).to be_redownload
        end
      end

      it "do not redownload if over 30 days old" do
        Timecop.freeze(Time.local(2018, 7, 24, 10, 5, 0)) do
          expect(@parser).not_to be_redownload
        end
      end
    end
  end

  describe "#valid?" do
    context "2018-06-24 hanshin 1R odds quinella place page" do
      it "is valid" do
        expect(@parser).to be_valid
      end
    end

    context "error page" do
      it "is invalid" do
        expect(@parser_error).not_to be_valid
      end
    end
  end

  describe "#related_links" do
    context "2018-06-24 hanshin 1R odds quinella place page" do
      it "is odds pages" do
        expect(@parser.related_links).to contain_exactly(
          "https://keiba.yahoo.co.jp/odds/tfw/1809030801/",
          "https://keiba.yahoo.co.jp/odds/ur/1809030801/",
          "https://keiba.yahoo.co.jp/odds/ut/1809030801/",
          "https://keiba.yahoo.co.jp/odds/sf/1809030801/",
          "https://keiba.yahoo.co.jp/odds/st/1809030801/")
      end
    end
  end

  describe "#parse" do
    context "2018-06-24 hanshin 1R odds quinella page" do
      it "is odds quinella info" do
        context = {}

        @parser.parse(context)

        # TODO: Parse all odds exacta info
        expect(context).to match(
          "odds_quinella_place" => {
            "1809030801" => {}
          }
        )
      end
    end

    context "valid page on web" do
      it "parse success" do
        parser = InvestmentHorseRacing::Crawler::Parser::OddsQuinellaPlacePageParser.new(@url, @downloader.download_with_get(@url))

        context = {}
        parser.parse(context)

        expect(context).to match(
          "odds_quinella_place" => {
            "1809030801" => {}
          }
        )
      end
    end
  end
end
