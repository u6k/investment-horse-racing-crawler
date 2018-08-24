module NetModule
  extend ActiveSupport::Concern

  def self.get_s3_bucket
    Aws.config.update({
      region: Rails.application.secrets.s3_region,
      credentials: Aws::Credentials.new(Rails.application.secrets.s3_access_key, Rails.application.secrets.s3_secret_key)
    })
    s3 = Aws::S3::Resource.new(endpoint: Rails.application.secrets.s3_endpoint, force_path_style: true)

    bucket = s3.bucket(Rails.application.secrets.s3_bucket)
  end

  def self.put_s3_object(bucket, file_name, data)
    # data compress
    data_7z = StringIO.new("")
    SevenZipRuby::Writer.open(data_7z) do |szr|
      szr.level = 9
      szr.add_data(data, file_name.split("/")[-1])
    end

    data_7z.rewind
    raise "Compress error" if not SevenZipRuby::Reader.verify(data_7z)

    data_7z.rewind
    data_7z = data_7z.read

    # upload
    obj_original = bucket.object(file_name + ".7z")
    obj_original.put(body: data_7z)

    obj_backup = bucket.object(file_name + ".7z.bak_" + DateTime.now.strftime("%Y%m%d-%H%M%S"))
    obj_backup.put(body: data_7z)

    { original: obj_original.key, backup: obj_backup.key }
  end

  def self.get_s3_object(bucket, file_name)
    # download
    object = bucket.object(file_name + ".7z")
    data_7z = object.get.body.read(object.size)

    # data extract
    data_7z = StringIO.new(data_7z)
    raise "Extract error" if not SevenZipRuby::Reader.verify(data_7z)

    data_7z.rewind

    data = nil
    SevenZipRuby::Reader.open(data_7z) do |szr|
      data = szr.extract_data(file_name.split("/")[-1])
    end

    data
  end

  def self.exists_s3_object?(bucket, file_name)
    bucket.object(file_name + ".7z").exists?
  end

  def self.download_with_get(url)
    uri = URI(url)

    req = Net::HTTP::Get.new(uri)
    req["User-Agent"] = "curl/7.54.0"
    req["Accept"] = "*/*"

    res = Net::HTTP.start(uri.hostname, uri.port, :use_ssl => uri.scheme == "https") do |http|
      http.request(req)
    end

    sleep(1)

    if res.code == "200"
      res.body
    else
      Rails.logger.warn "NetModule#download_with_get: status code not 200 ok: url=#{url}, code=#{res.code}"
      nil
    end
  end
end
