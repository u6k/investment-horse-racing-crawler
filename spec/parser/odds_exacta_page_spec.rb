require "timecop"

require "spec_helper"

RSpec.describe ScoringHorseRacing::Parser::OddsExactaPageParser do
  before do
    # 2018-06-24 hanshin 1R odds exacta page parser
    url = "https://keiba.yahoo.co.jp/odds/ut/1809030801/"
    data = File.open("spec/data/odds_exacta.20180624.hanshin.1.html").read

    @parser = ScoringHorseRacing::Parser::OddsExactaPageParser.new(url, data)

    # error page parser
    url = "https://keiba.yahoo.co.jp/odds/ut/0000000000/"
    data = File.open("spec/data/odds_exacta.00000000.error.html").read

    @parser_error = ScoringHorseRacing::Parser::OddsExactaPageParser.new(url, data)
  end

  describe "#redownload?" do
    context "2018-06-24 hanshin 1R odds exacta page" do
      it "redownload if newer than 2 months" do
        Timecop.freeze(Time.local(2018, 9, 21)) do
          expect(@parser).to be_redownload
        end
      end

      it "do not redownload if over 3 months old" do
        Timecop.freeze(Time.local(2018, 9, 22)) do
          expect(@parser).not_to be_redownload
        end
      end
    end
  end

  describe "#valid?" do
    context "2018-06-24 hanshin 1R odds exacta page" do
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
    context "2018-06-24 hanshin 1R odds exacta page" do
      it "is empty" do
        expect(@parser.related_links).to be_empty
      end
    end
  end

  describe "#parse" do
    context "2018-06-24 hanshin 1R odds exacta page" do
      it "is empty" do
        context = {}

        @parser.parse(context)

        # TODO: Parse all odds exacta info
        expect(context).to match(
          "odds_exacta" => {
            "1809030801" => {}
          }
        )
      end
    end
  end
end