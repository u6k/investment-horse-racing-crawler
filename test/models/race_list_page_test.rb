require 'test_helper'

class RaceListPageTest < ActiveSupport::TestCase

  def setup
    @bucket = NetModule.get_s3_bucket
    @bucket.objects.batch_delete!
  end

  test "download race list page" do
    # precondition
    course_list_page_html = File.open("test/fixtures/files/course_list/course_list.20180716.html").read
    NetModule.put_s3_object(NetModule.get_s3_bucket, "course_list/course_list.20180716.html", course_list_page_html)
    course_list_page = CourseListPage.new(date: Time.zone.local(2018, 7, 16, 0, 0, 0), url: "http://example.com/course_list.20180716.html")
    course_list_page.save!

    # execute 1
    race_list_pages = course_list_page.download_race_list_pages

    # postcondition 1
    assert_equal 5, race_list_pages.length

    race_list_pages.each do |race_list_page|
      assert_nil race_list_page.id
      assert race_list_page.content.length > 0
      assert race_list_page.valid?
    end

    assert_equal 1, CourseListPage.all.length
    assert_equal 0, RaceListPage.all.length

    assert_not @bucket.object("race_list/20180716/race_list.帯広競馬場.html").exists?
    assert_not @bucket.object("race_list/20180716/race_list.盛岡競馬場.html").exists?
    assert_not @bucket.object("race_list/20180716/race_list.名古屋競馬場.html").exists?
    assert_not @bucket.object("race_list/20180716/race_list.高知競馬場.html").exists?
    assert_not @bucket.object("race_list/20180716/race_list.佐賀競馬場.html").exists?

    # execute 2
    race_list_pages.each do |race_list_page|
      race_list_page.save!
    end

    # postcondition 2
    assert_equal 5, RaceListPage.all.length

    course_list_page.race_list_pages.each do |race_list_page_db|
      race_list_page = race_list_pages.find { |i| i.url == race_list_page_db.url }

      assert_equal race_list_page.same?(race_list_page_db)
    end

    assert @bucket.object("race_list/20180716/race_list.帯広競馬場.html").exists?
    assert @bucket.object("race_list/20180716/race_list.盛岡競馬場.html").exists?
    assert @bucket.object("race_list/20180716/race_list.名古屋競馬場.html").exists?
    assert @bucket.object("race_list/20180716/race_list.高知競馬場.html").exists?
    assert @bucket.object("race_list/20180716/race_list.佐賀競馬場.html").exists?

    # execute 3
    race_list_pages_2 = course_list_page.download_race_list_pages

    # postcondition 3
    assert_equal 5, RaceListPage.all.length

    race_list_pages_2.each do |race_list_page_2|
      assert_not_nil race_list_page_2.id
      assert race_list_page.content.length > 0
      assert race_list_page.valid?
    end

    # execute 4
    race_list_pages_2.each do |race_list_page_2|
      race_list_page_2.save!
    end

    # postcondition 4
    assert_equal 5, RaceListPage.all.length
  end

end
