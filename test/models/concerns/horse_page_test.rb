require 'test_helper'

class HorsePageTest < ActiveSupport::TestCase

  def setup
    @bucket = NetModule.get_s3_bucket
    @bucket.objects.batch_delete!
  end

  test "download" do
    # setup
    entry_page_html = File.open("test/fixtures/files/entry.20180624.hanshin.1.html").read
    entry_page = EntryPage.new("1809030801", entry_page_html)

    # execute - new
    entries = entry_page.entries

    # check
    assert_equal 0, HorsePage.find_all.length

    assert_equal 16, entries.length

    horse_page = entries[0][:horse]
    assert_equal "2015104308", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[1][:horse]
    assert_equal "2015104964", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[2][:horse]
    assert_equal "2015100632", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[3][:horse]
    assert_equal "2015100586", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[4][:horse]
    assert_equal "2015103335", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[5][:horse]
    assert_equal "2015104928", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[6][:horse]
    assert_equal "2015106259", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[7][:horse]
    assert_equal "2015102694", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[8][:horse]
    assert_equal "2015102837", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[9][:horse]
    assert_equal "2015105363", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[10][:horse]
    assert_equal "2015101618", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[11][:horse]
    assert_equal "2015102853", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[12][:horse]
    assert_equal "2015103462", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[13][:horse]
    assert_equal "2015103590", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[14][:horse]
    assert_equal "2015104979", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[15][:horse]
    assert_equal "2015103557", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    # execute - download
    entries.each { |e| e[:horse].download_from_web! }

    # check
    assert_equal 0, HorsePage.find_all.length

    assert_equal 16, entries.length

    horse_page = entries[0][:horse]
    assert_equal "2015104308", horse_page.horse_id
    assert_equal "$B%W%m%M%k%/!<%k(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[1][:horse]
    assert_equal "2015104964", horse_page.horse_id
    assert_equal "$B%9!<%V%l%C%H(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[2][:horse]
    assert_equal "2015100632", horse_page.horse_id
    assert_equal "$B%"%G%k(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[3][:horse]
    assert_equal "2015100586", horse_page.horse_id
    assert_equal "$B%d%^%K%s%U%#%*%C%3(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[4][:horse]
    assert_equal "2015103335", horse_page.horse_id
    assert_equal "$B%a%$%7%g%&%O%K!<(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[5][:horse]
    assert_equal "2015104928", horse_page.horse_id
    assert_equal "$B%l%s%V%i%s%5(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[6][:horse]
    assert_equal "2015106259", horse_page.horse_id
    assert_equal "$B%"%s%8%'%l%C%?(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[7][:horse]
    assert_equal "2015102694", horse_page.horse_id
    assert_equal "$B%F!<%*!<%Q!<%H%J!<(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[8][:horse]
    assert_equal "2015102837", horse_page.horse_id
    assert_equal "$B%&%$%s%?%$%`%j!<%W(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[9][:horse]
    assert_equal "2015105363", horse_page.horse_id
    assert_equal "$B%b%j%N%^%j%s(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[10][:horse]
    assert_equal "2015101618", horse_page.horse_id
    assert_equal "$B%W%m%`%/%$!<%s(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[11][:horse]
    assert_equal "2015102853", horse_page.horse_id
    assert_equal "$B%J%$%9%I%%(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[12][:horse]
    assert_equal "2015103462", horse_page.horse_id
    assert_equal "$B%"%/%"%l!<%L(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[13][:horse]
    assert_equal "2015103590", horse_page.horse_id
    assert_equal "$B%b%s%F%k!<%9(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[14][:horse]
    assert_equal "2015104979", horse_page.horse_id
    assert_equal "$B%j!<%:%s(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    horse_page = entries[15][:horse]
    assert_equal "2015103557", horse_page.horse_id
    assert_equal "$B%9%^!<%H%9%T%+(B", horse_page.horse_name
    assert horse_page.valid?
    assert_not horse_page.exists?

    # execute - save
    entries.each { |e| e[:horse].save! }

    # check
    assert_equal 16, HorsePage.find_all.length

    entries.each do |e|
      assert e[:horse].valid?
      assert e[:horse].exists?
    end

    # execute - re-new
    entry_page = EntryPage.new("1809030801", entry_page_html)
    entries_2 = entry_page.entries

    # check
    assert_equal 16, HorsePage.find_all.length

    assert_equal 16, entries_2.length

    horse_page_2 = entries_2[0][:horse]
    assert_equal "2015104308", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[1][:horse]
    assert_equal "2015104964", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[2][:horse]
    assert_equal "2015100632", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[3][:horse]
    assert_equal "2015100586", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[4][:horse]
    assert_equal "2015103335", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[5][:horse]
    assert_equal "2015104928", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[6][:horse]
    assert_equal "2015106259", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[7][:horse]
    assert_equal "2015102694", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[8][:horse]
    assert_equal "2015102837", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[9][:horse]
    assert_equal "2015105363", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[10][:horse]
    assert_equal "2015101618", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[11][:horse]
    assert_equal "2015102853", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[12][:horse]
    assert_equal "2015103462", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[13][:horse]
    assert_equal "2015103590", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[14][:horse]
    assert_equal "2015104979", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[15][:horse]
    assert_equal "2015103557", horse_page_2.horse_id
    assert_nil horse_page_2.horse_name
    assert_not horse_page_2.valid?
    assert horse_page_2.exists?

    # execute - download from s3
    entries_2.each { |e| e.download_from_s3! }

    # check
    assert_equal 16, HorsePage.find_all.length

    assert_equal 16, entries_2.length

    horse_page_2 = entries_2[0][:horse]
    assert_equal "2015104308", horse_page_2.horse_id
    assert_equal "$B%W%m%M%k%/!<%k(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[1][:horse]
    assert_equal "2015104964", horse_page_2.horse_id
    assert_equal "$B%9!<%V%l%C%H(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[2][:horse]
    assert_equal "2015100632", horse_page_2.horse_id
    assert_equal "$B%"%G%k(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[3][:horse]
    assert_equal "2015100586", horse_page_2.horse_id
    assert_equal "$B%d%^%K%s%U%#%*%C%3(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[4][:horse]
    assert_equal "2015103335", horse_page_2.horse_id
    assert_equal "$B%a%$%7%g%&%O%K!<(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[5][:horse]
    assert_equal "2015104928", horse_page_2.horse_id
    assert_equal "$B%l%s%V%i%s%5(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[6][:horse]
    assert_equal "2015106259", horse_page_2.horse_id
    assert_equal "$B%"%s%8%'%l%C%?(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[7][:horse]
    assert_equal "2015102694", horse_page_2.horse_id
    assert_equal "$B%F!<%*!<%Q!<%H%J!<(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[8][:horse]
    assert_equal "2015102837", horse_page_2.horse_id
    assert_equal "$B%&%$%s%?%$%`%j!<%W(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[9][:horse]
    assert_equal "2015105363", horse_page_2.horse_id
    assert_equal "$B%b%j%N%^%j%s(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[10][:horse]
    assert_equal "2015101618", horse_page_2.horse_id
    assert_equal "$B%W%m%`%/%$!<%s(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[11][:horse]
    assert_equal "2015102853", horse_page_2.horse_id
    assert_equal "$B%J%$%9%I%%(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[12][:horse]
    assert_equal "2015103462", horse_page_2.horse_id
    assert_equal "$B%"%/%"%l!<%L(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[13][:horse]
    assert_equal "2015103590", horse_page_2.horse_id
    assert_equal "$B%b%s%F%k!<%9(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[14][:horse]
    assert_equal "2015104979", horse_page_2.horse_id
    assert_equal "$B%j!<%:%s(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    horse_page_2 = entries_2[15][:horse]
    assert_equal "2015103557", horse_page_2.horse_id
    assert_equal "$B%9%^!<%H%9%T%+(B", horse_page_2.horse_name
    assert horse_page_2.valid?
    assert horse_page_2.exists?

    # execute - overwrite
    entries_2.each { |e| e.save! }

    # check
    assert_equal 16, HorsePage.find_all.length
  end

  test "download: invalid page" do
    # execute - new invalid page
    horse_page = HorsePage.new("0000000000")

    # check
    assert_equal 0, HorsePage.find_all.length

    assert_equal "0000000000", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    # execute - download -> fail
    horse_page.download_from_web!

    # check
    assert_equal 0, HorsePage.find_all.length

    assert_equal "0000000000", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?

    # execute - save -> fail
    assert_raises "Invalid" do
      horse_page.save!
    end

    # check
    assert_equal 0, HorsePage.find_all.length

    assert_equal "0000000000", horse_page.horse_id
    assert_nil horse_page.horse_name
    assert_not horse_page.valid?
    assert_not horse_page.exists?
  end

end
