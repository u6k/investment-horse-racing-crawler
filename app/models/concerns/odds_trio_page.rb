class OddsTrioPage
  extend ActiveSupport::Concern

  attr_reader :odds_id, :trio_results

  def self.find_all
    odds_trio_pages = NetModule.get_s3_bucket.objects(prefix: Rails.application.secrets.s3_folder + "/odds_trio/odds_trio.").map do |s3_obj|
      s3_obj.key.match(/odds_trio\.([0-9]+)\.html$/) do |path|
        OddsTrioPage.new(path[1])
      end
    end

    odds_trio_pages.compact
  end

  def initialize(odds_id, content = nil)
    @odds_id = odds_id
    @content = content

    _parse
  end

  def download_from_web!
    @content = NetModule.download_with_get(_build_url)

    _parse
  end

  def download_from_s3!
    @content = NetModule.get_s3_object(NetModule.get_s3_bucket, _build_s3_path)

    _parse
  end

  def valid?
    ((not @odds_id.nil?) \
      && (not @trio_results.nil?))
  end

  def exists?
    NetModule.get_s3_bucket.object(_build_s3_path).exists?
  end

  def save!
    if not valid?
      raise "Invalid"
    end

    NetModule.put_s3_object(NetModule.get_s3_bucket, _build_s3_path, @content)
  end

  def same?(obj)
    if not obj.instance_of?(OddsTrioPage)
      return false
    end

    if @odds_id != obj.odds_id \
      || @trio_results.nil? != obj.trio_results.nil?
      return false
    end

    true
  end

  private

  def _parse
    if @content.nil?
      return nil
    end

    doc = Nokogiri::HTML.parse(@content, nil, "UTF-8")

    doc.xpath("//li[@id='raceNavi2C']/a").each do |a|
      @trio_results = a.text
    end
  end

  def _build_url
    "https://keiba.yahoo.co.jp/odds/ut/#{@odds_id}/"
  end

  def _build_s3_path
    Rails.application.secrets.s3_folder + "/odds_trio/odds_trio.#{@odds_id}.html"
  end

end
