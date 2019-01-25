module ScoringHorseRacing::Rule
  class OddsQuinellaPage

    attr_reader :odds_id, :quinella_results

    def initialize(odds_id, content = nil)
      @odds_id = odds_id
      @content = content

      @downloader = Crawline::Downloader.new("scoring-horse-racing/0.0.0 (https://github.com/u6k/scoring-horse-racing")

      @repo = Crawline::ResourceRepository.new(
        Rails.application.secrets.s3_access_key,
        Rails.application.secrets.s3_secret_key,
        Rails.application.secrets.s3_region,
        Rails.application.secrets.s3_bucket,
        Rails.application.secrets.s3_endpoint,
        true)

      _parse
    end

    def download_from_web!
      begin
        @content = @downloader.download_with_get(_build_url)
      rescue
        # TODO: Logging warning
        @content = nil
      end

      _parse
    end

    def download_from_s3!
      @content = @repo.get_s3_object(_build_s3_path)

      _parse
    end

    def valid?
      ((not @odds_id.nil?) \
        && (not @quinella_results.nil?))
    end

    def exists?
      @repo.exists_s3_object?(_build_s3_path)
    end

    def save!
      if not valid?
        raise "Invalid"
      end

      @repo.put_s3_object(_build_s3_path, @content)
    end

    def same?(obj)
      if not obj.instance_of?(OddsQuinellaPage)
        return false
      end

      if @odds_id != obj.odds_id \
        || @quinella_results.nil? != obj.quinella_results.nil?
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
        @quinella_results = a.text
      end
    end

    def _build_url
      "https://keiba.yahoo.co.jp/odds/ur/#{@odds_id}/"
    end

    def _build_s3_path
      Rails.application.secrets.s3_folder + "/odds_quinella/odds_quinella.#{@odds_id}.html"
    end

  end
end