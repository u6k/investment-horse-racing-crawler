class HorsePage
  extend ActiveSupport::Concern

  attr_reader :horse_id, :horse_name

  def self.find_all
    horse_pages = NetModule.get_s3_bucket.objects(prefix: Rails.application.secrets.s3_folder + "/horse/horse.").map do |s3_obj|
      s3_obj.key.match(/horse\.([0-9]+)\.html\.7z$/) do |path|
        HorsePage.new(path[1])
      end
    end

    horse_pages.compact
  end

  def initialize(horse_id, content = nil)
    @horse_id = horse_id
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
    ((not @horse_id.nil?) \
      && (not @horse_name.nil?))
  end

  def exists?
    NetModule.exists_s3_object?(NetModule.get_s3_bucket, _build_s3_path)
  end

  def save!
    if not valid?
      raise "Invalid"
    end

    NetModule.put_s3_object(NetModule.get_s3_bucket, _build_s3_path, @content)
  end

  def same?(obj)
    if not obj.instance_of?(HorsePage)
      return false
    end

    if @horse_id != obj.horse_id \
      || @horse_name != obj.horse_name
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

    doc.xpath("//div[@id='dirTitName']/h1").each do |h1|
      @horse_name = h1.text.strip
    end
  end

  def _build_url
    "https://keiba.yahoo.co.jp/directory/horse/#{@horse_id}/"
  end

  def _build_s3_path
    Rails.application.secrets.s3_folder + "/horse/horse.#{horse_id}.html"
  end

end
